"""
Game Session model
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GameSession:
    """Represents a game session"""
    
    session_id: str
    language: str = 'en'
    category: str = 'all'
    status: str = 'playing'  # 'playing', 'guessing', 'finished'
    
    # Game state
    possible_places: List[str] = field(default_factory=list)  # Place IDs
    all_places: Dict[str, Any] = field(default_factory=dict)  # ID -> Place object
    answers: List[Dict[str, str]] = field(default_factory=list)
    current_question: Optional[Any] = None
    guess: Optional[str] = None  # Place ID
    correct: Optional[bool] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def questions_asked(self) -> int:
        """Number of questions asked so far"""
        return len(self.answers)
    
    def add_answer(self, question_id: str, answer: str):
        """Record an answer"""
        self.answers.append({
            'question_id': question_id,
            'answer': answer,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
        self.last_updated = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'session_id': self.session_id,
            'language': self.language,
            'category': self.category,
            'status': self.status,
            'possible_places': self.possible_places,
            'all_places': {k: v.to_dict() for k, v in self.all_places.items()},
            'answers': self.answers,
            'current_question': self.current_question.to_dict() if self.current_question else None,
            'guess': self.guess,
            'correct': self.correct,
            'created_at': self.created_at.isoformat() + 'Z',
            'last_updated': self.last_updated.isoformat() + 'Z'
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameSession':
        """Create from dictionary"""
        from app.models.place import Place
        from app.models.question import Question
        
        session = cls(
            session_id=data['session_id'],
            language=data.get('language', 'en'),
            category=data.get('category', 'all'),
            status=data.get('status', 'playing'),
            possible_places=data.get('possible_places', []),
            answers=data.get('answers', []),
            guess=data.get('guess'),
            correct=data.get('correct')
        )
        
        # Reconstruct all_places
        if 'all_places' in data:
            session.all_places = {
                k: Place.from_dict(v) for k, v in data['all_places'].items()
            }
        
        # Reconstruct current_question
        if data.get('current_question'):
            session.current_question = Question.from_dict(data['current_question'])
        
        # Parse timestamps
        if 'created_at' in data:
            session.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        if 'last_updated' in data:
            session.last_updated = datetime.fromisoformat(data['last_updated'].replace('Z', '+00:00'))
        
        return session