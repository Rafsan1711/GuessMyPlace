"""
Data Service - Manages loading and caching of places and questions
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from app.models.place import Place
from app.models.question import Question


class DataService:
    """Loads and manages game data"""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent.parent / 'data'
        self._places_cache = None
        self._questions_cache = None
    
    def get_places(self, category: str = 'all') -> List[Place]:
        """
        Get places filtered by category
        
        Args:
            category: 'all', 'countries', 'cities', 'historic_places'
            
        Returns:
            List of Place objects
        """
        if self._places_cache is None:
            self._load_places()
        
        if category == 'all':
            return self._places_cache
        
        # Filter by type
        type_map = {
            'countries': 'country',
            'cities': 'city',
            'historic_places': 'historic_place'
        }
        
        place_type = type_map.get(category)
        if not place_type:
            return self._places_cache
        
        return [p for p in self._places_cache if p.type == place_type]
    
    def get_place_by_id(self, place_id: str) -> Optional[Place]:
        """Get a specific place by ID"""
        if self._places_cache is None:
            self._load_places()
        
        for place in self._places_cache:
            if place.id == place_id:
                return place
        
        return None
    
    def get_questions(self) -> List[Question]:
        """Get all questions"""
        if self._questions_cache is None:
            self._load_questions()
        
        return self._questions_cache
    
    def reload_data(self):
        """Reload all data from files"""
        self._places_cache = None
        self._questions_cache = None
        self._load_places()
        self._load_questions()
    
    # Private methods
    
    def _load_places(self):
        """Load all places from data files"""
        all_places = []
        
        # Try to load combined file first
        combined_file = self.data_path / 'places' / 'combined.json'
        if combined_file.exists():
            with open(combined_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                places_data = data.get('places', [])
                all_places = [Place.from_dict(p) for p in places_data]
        else:
            # Load individual files
            for filename in ['countries.json', 'cities.json', 'historic_places.json']:
                file_path = self.data_path / 'places' / filename
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_places.extend([Place.from_dict(p) for p in data])
        
        self._places_cache = all_places
    
    def _load_questions(self):
        """Load all questions from data file"""
        questions_file = self.data_path / 'questions' / 'question_bank.json'
        
        if not questions_file.exists():
            self._questions_cache = []
            return
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self._questions_cache = [Question.from_dict(q) for q in data]