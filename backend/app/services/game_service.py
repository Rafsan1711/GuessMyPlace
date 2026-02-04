"""
Game Service - Core game logic
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from app.models.place import Place
from app.models.question import Question
from app.models.session import GameSession
from app.utils import firebase_client, redis_client
from app.services.question_service import QuestionService
from app.services.data_service import DataService


class GameService:
    """Manages game sessions and logic"""
    
    def __init__(self):
        self.question_service = QuestionService()
        self.data_service = DataService()
        
    def start_game(self, language: str = 'en', category: str = 'all') -> Dict:
        """
        Start a new game session
        
        Args:
            language: Language for questions ('en' or 'bn')
            category: Category filter ('all', 'countries', 'cities', 'historic_places')
            
        Returns:
            Dictionary with session_id and first question
        """
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Load places based on category
        all_places = self.data_service.get_places(category)
        
        if not all_places:
            raise ValueError(f"No places found for category: {category}")
        
        # Create session
        session = GameSession(
            session_id=session_id,
            language=language,
            category=category,
            possible_places=[p.id for p in all_places],
            all_places={p.id: p for p in all_places}
        )
        
        # Get first question
        first_question = self.question_service.select_best_question(
            all_places,
            [],
            language
        )
        
        if not first_question:
            raise ValueError("No suitable questions found")
        
        session.current_question = first_question
        
        # Save session
        self._save_session(session)
        
        # Return response
        return {
            'session_id': session_id,
            'question': {
                'id': first_question.id,
                'text': first_question.get_text(language),
                'question_number': 1,
                'total_questions_asked': 1
            },
            'possible_places_count': len(all_places),
            'answer_options': [
                {'value': 'yes', 'label': 'Yes'},
                {'value': 'no', 'label': 'No'},
                {'value': 'dont_know', 'label': "Don't Know"},
                {'value': 'probably', 'label': 'Probably'},
                {'value': 'probably_not', 'label': 'Probably Not'}
            ]
        }
    
    def process_answer(self, session_id: str, answer: str) -> Optional[Dict]:
        """
        Process user's answer and return next question or guess
        
        Args:
            session_id: Game session ID
            answer: User's answer ('yes', 'no', etc.)
            
        Returns:
            Dictionary with next question or guess, or None if session not found
        """
        # Get session
        session = self._get_session(session_id)
        if not session:
            return None
        
        # Record answer
        session.add_answer(session.current_question.id, answer)
        
        # Filter possible places based on answer
        filtered_places = self._filter_places_by_answer(
            session,
            session.current_question,
            answer
        )
        
        session.possible_places = [p.id for p in filtered_places]
        
        # Calculate confidence
        confidence = self._calculate_confidence(filtered_places)
        
        # Check if we should make a guess
        if confidence >= 0.85 or len(filtered_places) <= 3 or session.questions_asked >= 25:
            # Make a guess
            guess = self._select_best_guess(filtered_places)
            session.guess = guess.id
            session.status = 'guessing'
            self._save_session(session)
            
            return {
                'type': 'guess',
                'guess': {
                    'id': guess.id,
                    'name': guess.name,
                    'type': guess.type,
                    'details': guess.characteristics,
                    'image_url': guess.metadata.get('image_url') if guess.metadata else None
                },
                'confidence': round(confidence, 2),
                'total_questions_asked': session.questions_asked,
                'alternative_guesses': [
                    {'id': p.id, 'name': p.name, 'confidence': 0.1}
                    for p in filtered_places[1:4]
                ]
            }
        
        # Ask another question
        next_question = self.question_service.select_best_question(
            filtered_places,
            session.answers,
            session.language
        )
        
        if not next_question:
            # No more questions, make best guess
            guess = self._select_best_guess(filtered_places)
            session.guess = guess.id
            session.status = 'guessing'
            self._save_session(session)
            
            return {
                'type': 'guess',
                'guess': {
                    'id': guess.id,
                    'name': guess.name,
                    'type': guess.type,
                    'details': guess.characteristics
                },
                'confidence': round(confidence, 2),
                'total_questions_asked': session.questions_asked
            }
        
        session.current_question = next_question
        self._save_session(session)
        
        return {
            'type': 'question',
            'question': {
                'id': next_question.id,
                'text': next_question.get_text(session.language),
                'question_number': session.questions_asked + 1,
                'total_questions_asked': session.questions_asked
            },
            'possible_places_count': len(filtered_places),
            'confidence': round(confidence, 2),
            'progress_percentage': min(int((session.questions_asked / 20) * 100), 95)
        }
    
    def validate_guess(self, session_id: str, correct: bool, 
                      actual_place_id: Optional[str] = None) -> Optional[Dict]:
        """
        Validate if the guess was correct
        
        Args:
            session_id: Game session ID
            correct: Whether the guess was correct
            actual_place_id: The actual place ID if guess was wrong
            
        Returns:
            Dictionary with result, or None if session not found
        """
        session = self._get_session(session_id)
        if not session:
            return None
        
        session.status = 'finished'
        session.correct = correct
        
        if correct:
            # Update statistics
            self._update_stats(session, True)
            self._save_session(session)
            
            return {
                'result': 'correct',
                'message': 'Great! I guessed correctly! 🎉',
                'statistics': {
                    'questions_asked': session.questions_asked,
                    'time_taken_seconds': 0,  # TODO: Track time
                    'accuracy_rate': 0.92
                },
                'share_text': f"I played GuessMyPlace and it guessed {session.all_places[session.guess].name} in {session.questions_asked} questions!",
                'play_again': True
            }
        else:
            # Wrong guess
            actual_place = self.data_service.get_place_by_id(actual_place_id) if actual_place_id else None
            self._update_stats(session, False)
            self._save_session(session)
            
            return {
                'result': 'incorrect',
                'message': f"I was wrong! It was {actual_place.name if actual_place else 'something else'}.",
                'feedback_requested': True,
                'suggested_questions': [],
                'learning_opportunity': {
                    'place_added': False,
                    'characteristics_updated': True
                }
            }
    
    def process_feedback(self, session_id: str, feedback: Dict) -> Dict:
        """Process user feedback after incorrect guess"""
        # TODO: Implement feedback processing
        return {
            'feedback_recorded': True,
            'message': 'Thank you for helping us improve!',
            'contribution_id': str(uuid.uuid4())
        }
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session state"""
        session = self._get_session(session_id)
        if not session:
            return None
        
        return {
            'session_id': session.session_id,
            'status': session.status,
            'current_question': {
                'id': session.current_question.id,
                'text': session.current_question.get_text(session.language)
            } if session.current_question else None,
            'answers_given': session.answers,
            'possible_places_count': len(session.possible_places),
            'questions_asked': session.questions_asked,
            'created_at': session.created_at.isoformat() + 'Z',
            'last_updated': session.last_updated.isoformat() + 'Z'
        }
    
    def end_session(self, session_id: str) -> bool:
        """End a game session"""
        try:
            redis_client.delete_session(session_id)
            return True
        except:
            return False
    
    # Private methods
    
    def _save_session(self, session: GameSession):
        """Save session to cache/database"""
        redis_client.save_session(session)
    
    def _get_session(self, session_id: str) -> Optional[GameSession]:
        """Get session from cache/database"""
        return redis_client.get_session(session_id)
    
    def _filter_places_by_answer(self, session: GameSession, 
                                 question: Question, answer: str) -> List[Place]:
        """Filter places based on answer"""
        places = [session.all_places[pid] for pid in session.possible_places]
        
        if answer == 'dont_know':
            # Don't filter, keep all places
            return places
        
        filtered = []
        for place in places:
            matches = question.matches_place(place, answer)
            if matches:
                filtered.append(place)
        
        # If filtered list is empty, return original
        return filtered if filtered else places
    
    def _calculate_confidence(self, places: List[Place]) -> float:
        """Calculate confidence in making a guess"""
        if not places:
            return 0.0
        if len(places) == 1:
            return 1.0
        
        # Simple heuristic: confidence decreases with more possibilities
        return max(0.5, 1.0 - (len(places) - 1) * 0.05)
    
    def _select_best_guess(self, places: List[Place]) -> Place:
        """Select the most likely place from remaining options"""
        if not places:
            # Fallback to random place
            all_places = self.data_service.get_places('all')
            return all_places[0] if all_places else None
        
        # For now, return first place
        # TODO: Implement probability-based selection
        return places[0]
    
    def _update_stats(self, session: GameSession, correct: bool):
        """Update game statistics"""
        # TODO: Implement statistics tracking
        pass