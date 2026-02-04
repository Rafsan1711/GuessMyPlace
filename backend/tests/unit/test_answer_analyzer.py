"""
Unit tests for AnswerAnalyzer
"""

import pytest
from algorithms.python.answer_analyzer import AnswerAnalyzer


class TestAnswerAnalyzer:
    
    def test_detect_contradictions_none(self):
        """Test contradiction detection with consistent answers"""
        answers = [
            {
                'question_id': 'q1',
                'characteristic': 'continent',
                'answer': 'yes'
            },
            {
                'question_id': 'q2',
                'characteristic': 'population',
                'answer': 'yes'
            }
        ]
        
        contradictions = AnswerAnalyzer.detect_contradictions(answers)
        assert len(contradictions) == 0
    
    def test_detect_contradictions_found(self):
        """Test contradiction detection with conflicting answers"""
        answers = [
            {
                'question_id': 'q1',
                'characteristic': 'continent',
                'answer': 'yes'
            },
            {
                'question_id': 'q2',
                'characteristic': 'continent',
                'answer': 'no'
            }
        ]
        
        contradictions = AnswerAnalyzer.detect_contradictions(answers)
        assert len(contradictions) > 0
    
    def test_calculate_answer_confidence_high(self):
        """Test confidence calculation with definite answers"""
        answers = [
            {'answer': 'yes'},
            {'answer': 'no'},
            {'answer': 'yes'}
        ]
        
        confidence = AnswerAnalyzer.calculate_answer_confidence(answers)
        assert confidence == 1.0
    
    def test_calculate_answer_confidence_low(self):
        """Test confidence calculation with uncertain answers"""
        answers = [
            {'answer': 'dont_know'},
            {'answer': 'dont_know'}
        ]
        
        confidence = AnswerAnalyzer.calculate_answer_confidence(answers)
        assert confidence == 0.0
    
    def test_calculate_answer_confidence_mixed(self):
        """Test confidence calculation with mixed answers"""
        answers = [
            {'answer': 'yes'},
            {'answer': 'probably'},
            {'answer': 'dont_know'}
        ]
        
        confidence = AnswerAnalyzer.calculate_answer_confidence(answers)
        assert 0.0 < confidence < 1.0
    
    def test_identify_key_characteristics(self):
        """Test identification of confidently known characteristics"""
        answers = [
            {
                'characteristic': 'continent',
                'answer': 'yes'
            },
            {
                'characteristic': 'population',
                'answer': 'probably'
            },
            {
                'characteristic': 'climate',
                'answer': 'dont_know'
            }
        ]
        
        key_chars = AnswerAnalyzer.identify_key_characteristics(answers)
        
        assert 'continent' in key_chars
        assert 'population' not in key_chars  # Below 0.8 threshold
        assert 'climate' not in key_chars
    
    def test_analyze_answer_distribution(self):
        """Test answer distribution analysis"""
        answers = [
            {'answer': 'yes'},
            {'answer': 'yes'},
            {'answer': 'no'},
            {'answer': 'probably'}
        ]
        
        distribution = AnswerAnalyzer.analyze_answer_distribution(answers)
        
        assert distribution['yes'] == 2
        assert distribution['no'] == 1
        assert distribution['probably'] == 1
    
    def test_calculate_progress_score(self):
        """Test progress score calculation"""
        answers = [
            {'answer': 'yes'},
            {'answer': 'no'}
        ]
        
        progress = AnswerAnalyzer.calculate_progress_score(
            answers, 
            total_places=100,
            remaining_places=10
        )
        
        # Should show significant progress (90% eliminated)
        assert progress > 0.5
    
    def test_estimate_questions_remaining(self):
        """Test estimation of remaining questions"""
        # With 8 places remaining
        estimate = AnswerAnalyzer.estimate_questions_remaining(
            remaining_places=8,
            average_elimination_rate=0.5
        )
        
        # Should estimate ~3 questions (log2(8) = 3)
        assert 2 <= estimate <= 4
    
    def test_estimate_questions_one_place(self):
        """Test estimation with one place remaining"""
        estimate = AnswerAnalyzer.estimate_questions_remaining(
            remaining_places=1
        )
        
        assert estimate == 0
    
    def test_suggest_clarifying_questions(self):
        """Test clarifying question suggestions"""
        answers = [
            {
                'question_id': 'q1',
                'characteristic': 'continent',
                'answer': 'probably'
            }
        ]
        
        all_questions = [
            {
                'id': 'q1',
                'characteristic': 'continent'
            },
            {
                'id': 'q2',
                'characteristic': 'continent'
            },
            {
                'id': 'q3',
                'characteristic': 'population'
            }
        ]
        
        suggestions = AnswerAnalyzer.suggest_clarifying_questions(
            answers, all_questions
        )
        
        # Should suggest q2 (same char, not asked)
        suggested_ids = [q['id'] for q in suggestions]
        assert 'q2' in suggested_ids
        assert 'q1' not in suggested_ids  # Already asked