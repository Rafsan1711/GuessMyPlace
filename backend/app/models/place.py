"""
Place model
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Place:
    """Represents a place (country, city, or historic place)"""
    
    id: str
    name: str
    type: str  # 'country', 'city', 'historic_place'
    characteristics: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    aliases: List[str] = field(default_factory=list)
    
    def has_characteristic(self, key: str) -> bool:
        """Check if place has a characteristic"""
        return key in self.characteristics
    
    def get_characteristic(self, key: str, default: Any = None) -> Any:
        """Get characteristic value"""
        return self.characteristics.get(key, default)
    
    def matches_value(self, key: str, value: Any, operator: str = 'equals') -> bool:
        """
        Check if characteristic matches a value with given operator
        
        Args:
            key: Characteristic key
            value: Value to compare
            operator: Comparison operator
            
        Returns:
            True if matches, False otherwise
        """
        if not self.has_characteristic(key):
            return False
        
        char_value = self.get_characteristic(key)
        
        if operator == 'equals':
            return char_value == value
        elif operator == 'not_equals':
            return char_value != value
        elif operator == 'greater_than':
            return char_value > value
        elif operator == 'less_than':
            return char_value < value
        elif operator == 'greater_or_equal':
            return char_value >= value
        elif operator == 'less_or_equal':
            return char_value <= value
        elif operator == 'contains':
            if isinstance(char_value, list):
                return value in char_value
            return value in str(char_value)
        elif operator == 'not_contains':
            if isinstance(char_value, list):
                return value not in char_value
            return value not in str(char_value)
        
        return False
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Place':
        """Create Place from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            type=data['type'],
            characteristics=data['characteristics'],
            metadata=data.get('metadata'),
            aliases=data.get('aliases', [])
        )
    
    def to_dict(self) -> Dict:
        """Convert Place to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'characteristics': self.characteristics,
            'metadata': self.metadata,
            'aliases': self.aliases
        }