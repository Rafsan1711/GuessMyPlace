"""
Request validators
"""

from typing import Dict, List, Optional, Any
from flask import request


def validate_request(required_fields: List[str]) -> Optional[Dict[str, str]]:
    """
    Validate request has required fields
    
    Args:
        required_fields: List of required field names
        
    Returns:
        Error dict if validation fails, None if success
    """
    data = request.get_json()
    
    if not data:
        return {
            'code': 'INVALID_REQUEST',
            'message': 'Request body is required'
        }
    
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            'code': 'INVALID_REQUEST',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }
    
    return None


def validate_language(language: str) -> bool:
    """Validate language code"""
    return language in ['en', 'bn']


def validate_category(category: str) -> bool:
    """Validate place category"""
    return category in ['all', 'countries', 'cities', 'historic_places']


def validate_answer(answer: str) -> bool:
    """Validate answer value"""
    return answer in ['yes', 'no', 'dont_know', 'probably', 'probably_not']