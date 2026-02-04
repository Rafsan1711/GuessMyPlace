"""
Question model
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Question:
    """Represents a question"""
    
    id: str
    text: Dict[str, str]  # {'en': '...', 'bn': '...'}
    characteristic: str
    value: Any
    operator: str = 'equals'
    discriminating_power: float = 0.5
    category: str = 'general'
    applies_to: List[str] = field(default_factory=lambda: ['country', 'city', 'historic_place'])
    metadata: Optional[Dict[str, Any]] = None
    
    def get_text(self, language: str = 'en') -> str:
        """Get question text in specified language"""
        return self.text.get(language, self.text.get('en', ''))
    
    def matches_place(self, place, answer: str) -> bool:
        """
        Check if a place matches this question based on answer
        
        Args:
            place: Place object
            answer: User's answer ('yes', 'no', 'probably', etc.)
            
        Returns:
            True if place should be kept, False if filtered out
        """
        from app.models.place import Place
        
        # Map answers to boolean/probability
        if answer == 'yes':
            # Place must match the question
            return place.matches_value(self.characteristic, self.value, self.operator)
        elif answer == 'no':
            # Place must NOT match the question
            return not place.matches_value(self.characteristic, self.value, self.operator)
        elif answer == 'probably':
            # Keep places that match (70% confidence)
            return place.matches_value(self.characteristic, self.value, self.operator)
        elif answer == 'probably_not':
            # Keep places that don't match (70% confidence)
            return not place.matches_value(self.characteristic, self.value, self.operator)
        elif answer == 'dont_know':
            # Keep all places (no filtering)
            return True
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Question':
        """Create Question from dictionary"""
        return cls(
            id=data['id'],
            text=data['text'],
            characteristic=data['characteristic'],
            value=data['value'],
            operator=data.get('operator', 'equals'),
            discriminating_power=data.get('discriminating_power', 0.5),
            category=data.get('category', 'general'),
            applies_to=data.get('applies_to', ['country', 'city', 'historic_place']),
            metadata=data.get('metadata')
        )
    
    def to_dict(self) -> Dict:
        """Convert Question to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'characteristic': self.characteristic,
            'value': self.value,
            'operator': self.operator,
            'discriminating_power': self.discriminating_power,
            'category': self.category,
            'applies_to': self.applies_to,
            'metadata': self.metadata
        }