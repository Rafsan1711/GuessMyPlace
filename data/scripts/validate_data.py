#!/usr/bin/env python3
"""
Data Validation Script for GuessMyPlace
Validates all data files against their schemas
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.END} {msg}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")


def print_header(msg: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


class DataValidator:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.errors = []
        self.warnings = []
        
    def validate_id_format(self, id_str: str, item_type: str) -> bool:
        """Validate ID format"""
        if item_type == "question":
            pattern = r'^q_[0-9]{3,4}$'
            if not re.match(pattern, id_str):
                return False
        else:
            pattern = r'^[a-z0-9_]+$'
            if not re.match(pattern, id_str):
                return False
        return True
    
    def validate_place(self, place: Dict, index: int) -> Tuple[bool, List[str]]:
        """Validate a single place"""
        errors = []
        
        # Required fields
        required_fields = ['id', 'name', 'type', 'characteristics']
        for field in required_fields:
            if field not in place:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Validate ID format
        if not self.validate_id_format(place['id'], 'place'):
            errors.append(f"Invalid ID format: {place['id']} (must be snake_case)")
        
        # Validate type
        valid_types = ['country', 'city', 'historic_place']
        if place['type'] not in valid_types:
            errors.append(f"Invalid type: {place['type']}")
        
        # Validate characteristics
        chars = place.get('characteristics', {})
        if len(chars) < 5:
            errors.append(f"Too few characteristics: {len(chars)} (minimum 5)")
        
        # Check for required characteristics
        if 'continent' not in chars:
            errors.append("Missing 'continent' characteristic")
        
        if place['type'] != 'country' and 'country' not in chars:
            errors.append("Missing 'country' characteristic")
        
        # Validate continent value
        valid_continents = [
            'africa', 'antarctica', 'asia', 'europe',
            'north_america', 'oceania', 'south_america'
        ]
        if 'continent' in chars and chars['continent'] not in valid_continents:
            errors.append(f"Invalid continent: {chars['continent']}")
        
        # Validate numeric values
        if 'population_millions' in chars:
            pop = chars['population_millions']
            if not isinstance(pop, (int, float)) or pop < 0:
                errors.append(f"Invalid population: {pop}")
        
        if 'built_year' in chars:
            year = chars['built_year']
            if not isinstance(year, int):
                errors.append(f"Invalid built_year: {year} (must be integer)")
        
        # Validate metadata if present
        if 'metadata' in place:
            meta = place['metadata']
            if 'added_date' in meta:
                try:
                    datetime.fromisoformat(meta['added_date'].replace('Z', '+00:00'))
                except ValueError:
                    errors.append(f"Invalid date format: {meta['added_date']}")
        
        return len(errors) == 0, errors
    
    def validate_question(self, question: Dict, index: int) -> Tuple[bool, List[str]]:
        """Validate a single question"""
        errors = []
        
        # Required fields
        required_fields = ['id', 'text', 'characteristic', 'discriminating_power', 'category']
        for field in required_fields:
            if field not in question:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Validate ID format
        if not self.validate_id_format(question['id'], 'question'):
            errors.append(f"Invalid ID format: {question['id']} (must be q_NNN)")
        
        # Validate text
        if 'text' in question:
            if not isinstance(question['text'], dict):
                errors.append("'text' must be an object")
            elif 'en' not in question['text']:
                errors.append("Missing English text")
            elif len(question['text']['en']) < 5:
                errors.append("Question text too short")
        
        # Validate discriminating_power
        if 'discriminating_power' in question:
            power = question['discriminating_power']
            if not isinstance(power, (int, float)):
                errors.append(f"Invalid discriminating_power type: {type(power)}")
            elif power < 0.0 or power > 1.0:
                errors.append(f"discriminating_power out of range: {power}")
        
        # Validate category
        valid_categories = [
            'location', 'physical', 'temporal', 'classification',
            'cultural', 'functional', 'political', 'natural',
            'historical', 'architectural'
        ]
        if 'category' in question and question['category'] not in valid_categories:
            errors.append(f"Invalid category: {question['category']}")
        
        # Validate operator if present
        if 'operator' in question:
            valid_operators = [
                'equals', 'not_equals', 'greater_than', 'less_than',
                'greater_or_equal', 'less_or_equal', 'contains',
                'not_contains', 'in_range'
            ]
            if question['operator'] not in valid_operators:
                errors.append(f"Invalid operator: {question['operator']}")
        
        # Validate applies_to if present
        if 'applies_to' in question:
            valid_types = ['country', 'city', 'historic_place']
            applies_to = question['applies_to']
            if not isinstance(applies_to, list):
                errors.append("'applies_to' must be an array")
            else:
                for t in applies_to:
                    if t not in valid_types:
                        errors.append(f"Invalid type in applies_to: {t}")
        
        return len(errors) == 0, errors
    
    def validate_file(self, file_path: Path, item_type: str) -> bool:
        """Validate a JSON data file"""
        print_info(f"Validating {file_path.name}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in {file_path.name}: {e}")
            return False
        except FileNotFoundError:
            print_warning(f"File not found: {file_path.name}")
            return True  # Skip missing files
        
        if not isinstance(data, list):
            print_error(f"{file_path.name} must contain an array")
            return False
        
        # Check for duplicates
        ids = [item.get('id') for item in data]
        duplicates = [id for id in ids if ids.count(id) > 1]
        if duplicates:
            print_error(f"Duplicate IDs found: {set(duplicates)}")
            return False
        
        # Validate each item
        all_valid = True
        for i, item in enumerate(data):
            if item_type == 'question':
                valid, errors = self.validate_question(item, i)
            else:
                valid, errors = self.validate_place(item, i)
            
            if not valid:
                all_valid = False
                item_id = item.get('id', f'item_{i}')
                print_error(f"  {item_id}:")
                for error in errors:
                    print(f"    - {error}")
        
        if all_valid:
            print_success(f"{file_path.name}: {len(data)} items validated")
        
        return all_valid
    
    def validate_all(self) -> bool:
        """Validate all data files"""
        print_header("GuessMyPlace Data Validation")
        
        all_valid = True
        
        # Validate place files
        print_header("Validating Places")
        place_files = [
            ('places/countries.json', 'country'),
            ('places/cities.json', 'city'),
            ('places/historic_places.json', 'historic_place'),
        ]
        
        for file_path, item_type in place_files:
            full_path = self.data_dir / file_path
            if not self.validate_file(full_path, item_type):
                all_valid = False
        
        # Validate question file
        print_header("Validating Questions")
        question_file = self.data_dir / 'questions' / 'question_bank.json'
        if not self.validate_file(question_file, 'question'):
            all_valid = False
        
        # Summary
        print_header("Validation Summary")
        if all_valid:
            print_success("All data files are valid! ✨")
        else:
            print_error("Validation failed. Please fix the errors above.")
        
        return all_valid


def main():
    """Main entry point"""
    # Get data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent
    
    # Create validator
    validator = DataValidator(data_dir)
    
    # Run validation
    is_valid = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()