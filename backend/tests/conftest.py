"""
Pytest configuration and fixtures
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app


@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_places():
    """Sample place data for testing"""
    return [
        {
            'id': 'france',
            'name': 'France',
            'type': 'country',
            'characteristics': {
                'continent': 'europe',
                'population_millions': 67,
                'eu_member': True
            }
        },
        {
            'id': 'japan',
            'name': 'Japan',
            'type': 'country',
            'characteristics': {
                'continent': 'asia',
                'population_millions': 125,
                'is_island': True
            }
        },
        {
            'id': 'paris',
            'name': 'Paris',
            'type': 'city',
            'characteristics': {
                'continent': 'europe',
                'country': 'france',
                'is_capital': True
            }
        }
    ]


@pytest.fixture
def sample_questions():
    """Sample question data for testing"""
    return [
        {
            'id': 'q_001',
            'text': {'en': 'Is it in Europe?', 'bn': 'এটি কি ইউরোপে?'},
            'characteristic': 'continent',
            'value': 'europe',
            'operator': 'equals',
            'discriminating_power': 0.95,
            'category': 'location'
        },
        {
            'id': 'q_010',
            'text': {'en': 'Is it a capital?', 'bn': 'এটি কি রাজধানী?'},
            'characteristic': 'is_capital',
            'value': True,
            'operator': 'equals',
            'discriminating_power': 0.75,
            'category': 'classification'
        }
    ]