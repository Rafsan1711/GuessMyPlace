"""
Question Service - Question selection logic
"""

from typing import List, Dict, Optional
from app.models.place import Place
from app.models.question import Question
from app.services.data_service import DataService
import random


class QuestionService:
    """Manages question selection and scoring"""
    
    def __init__(self):
        self.data_service = DataService()
        self.questions = self.data_service.get_questions()
    
    def select_best_question(self, possible_places: List[Place], 
                            asked_questions: List[Dict],
                            language: str = 'en') -> Optional[Question]:
        """
        Select the best next question based on information gain
        
        Args:
            possible_places: List of currently possible places
            asked_questions: List of already asked questions
            language: Language for the question
            
        Returns:
            Best question to ask, or None if no suitable questions
        """
        if not possible_places:
            return None
        
        # Get already asked question IDs
        asked_ids = {q['question_id'] for q in asked_questions}
        
        # Filter applicable questions
        available_questions = []
        for question in self.questions:
            # Skip already asked
            if question.id in asked_ids:
                continue
            
            # Check if question applies to current place types
            place_types = {p.type for p in possible_places}
            if not any(t in question.applies_to for t in place_types):
                continue
            
            available_questions.append(question)
        
        if not available_questions:
            return None
        
        # Score each question by information gain
        scored_questions = []
        for question in available_questions:
            score = self._calculate_information_gain(question, possible_places)
            scored_questions.append((score, question))
        
        # Sort by score (descending)
        scored_questions.sort(reverse=True, key=lambda x: x[0])
        
        # Return best question
        if scored_questions:
            return scored_questions[0][1]
        
        return None
    
    def _calculate_information_gain(self, question: Question, 
                                   places: List[Place]) -> float:
        """
        Calculate information gain for a question
        
        Information gain measures how well a question splits the dataset.
        Higher is better.
        """
        if not places:
            return 0.0
        
        # Count how many places would match "yes" vs "no"
        yes_count = 0
        no_count = 0
        
        for place in places:
            if question.matches_place(place, 'yes'):
                yes_count += 1
            else:
                no_count += 1
        
        # Perfect split (50/50) has highest information gain
        # Calculate how close to 50/50 the split is
        total = len(places)
        yes_ratio = yes_count / total if total > 0 else 0
        no_ratio = no_count / total if total > 0 else 0
        
        # Entropy-based calculation
        # Perfect split: both ratios = 0.5, entropy = 1.0
        # Bad split: one ratio = 1.0, entropy = 0.0
        import math
        
        def entropy(ratio):
            if ratio == 0 or ratio == 1:
                return 0
            return -ratio * math.log2(ratio)
        
        information_gain = entropy(yes_ratio) + entropy(no_ratio)
        
        # Add bonus for question's discriminating power
        information_gain *= question.discriminating_power
        
        return information_gain