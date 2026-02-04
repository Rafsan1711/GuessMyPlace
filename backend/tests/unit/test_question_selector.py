"""
Unit tests for QuestionSelector
"""

import pytest
import math
from algorithms.python.question_selector import QuestionSelector


class TestQuestionSelector:
    
    def test_calculate_entropy_uniform(self):
        """Test entropy calculation with uniform distribution"""
        distribution = {'A': 1, 'B': 1, 'C': 1, 'D': 1}
        entropy = QuestionSelector.calculate_entropy(distribution)
        
        # Uniform distribution of 4 items: log2(4) = 2.0
        assert abs(entropy - 2.0) < 0.001
    
    def test_calculate_entropy_pure(self):
        """Test entropy calculation with pure distribution"""
        distribution = {'A': 10}
        entropy = QuestionSelector.calculate_entropy(distribution)
        
        # Pure distribution: entropy = 0
        assert abs(entropy) < 0.001
    
    def test_calculate_entropy_empty(self):
        """Test entropy with empty distribution"""
        distribution = {}
        entropy = QuestionSelector.calculate_entropy(distribution)
        
        assert entropy == 0.0
    
    def test_calculate_gini_impurity_pure(self):
        """Test Gini impurity with pure distribution"""
        distribution = {'A': 10}
        gini = QuestionSelector.calculate_gini_impurity(distribution)
        
        # Pure distribution: Gini = 0
        assert abs(gini) < 0.001
    
    def test_calculate_gini_impurity_split(self):
        """Test Gini impurity with 50-50 split"""
        distribution = {'A': 5, 'B': 5}
        gini = QuestionSelector.calculate_gini_impurity(distribution)
        
        # 50-50 split: Gini = 0.5
        assert abs(gini - 0.5) < 0.001
    
    def test_information_gain_ratio(self):
        """Test information gain ratio calculation"""
        parent = {'type1': 5, 'type2': 5}
        left = {'type1': 5}
        right = {'type2': 5}
        
        gain_ratio = QuestionSelector.calculate_information_gain_ratio(
            parent, left, right
        )
        
        # Perfect split should have high gain ratio
        assert gain_ratio > 0.5
    
    def test_select_by_variance_reduction(self):
        """Test question selection by variance reduction"""
        places = [
            {
                'id': 'france',
                'type': 'country',
                'characteristics': {'continent': 'europe'}
            },
            {
                'id': 'japan',
                'type': 'country',
                'characteristics': {'continent': 'asia'}
            }
        ]
        
        questions = [
            {
                'id': 'q1',
                'characteristic': 'continent',
                'value': 'europe',
                'operator': 'equals'
            }
        ]
        
        best_q = QuestionSelector.select_by_variance_reduction(
            places, questions, 'type'
        )
        
        assert best_q is not None
        assert best_q['id'] == 'q1'
    
    def test_matches_question_equals(self):
        """Test place matching with equals operator"""
        place = {
            'characteristics': {'continent': 'europe'}
        }
        question = {
            'characteristic': 'continent',
            'value': 'europe',
            'operator': 'equals'
        }
        
        matches = QuestionSelector._matches_question(place, question)
        assert matches is True
    
    def test_matches_question_greater_than(self):
        """Test place matching with greater_than operator"""
        place = {
            'characteristics': {'population': '100'}
        }
        question = {
            'characteristic': 'population',
            'value': '50',
            'operator': 'greater_than'
        }
        
        matches = QuestionSelector._matches_question(place, question)
        assert matches is True
    
    def test_matches_question_missing_characteristic(self):
        """Test matching when characteristic is missing"""
        place = {
            'characteristics': {'continent': 'europe'}
        }
        question = {
            'characteristic': 'population',
            'value': '100',
            'operator': 'equals'
        }
        
        matches = QuestionSelector._matches_question(place, question)
        assert matches is False