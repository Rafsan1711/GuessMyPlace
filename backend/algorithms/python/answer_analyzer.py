"""
Answer analysis and pattern detection
"""

from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict


class AnswerAnalyzer:
    """Analyzes answer patterns and provides insights"""
    
    @staticmethod
    def detect_contradictions(answers: List[Dict]) -> List[Tuple[str, str]]:
        """
        Detect contradictory answers in the session
        
        Args:
            answers: List of answer dictionaries
            
        Returns:
            List of (question_id1, question_id2) tuples that contradict
        """
        contradictions = []
        
        # Group answers by characteristic
        char_answers = defaultdict(list)
        for ans in answers:
            char = ans.get('characteristic')
            if char:
                char_answers[char].append(ans)
        
        # Check for contradictions within same characteristic
        for char, ans_list in char_answers.items():
            if len(ans_list) > 1:
                # Check if answers conflict
                values = [a.get('answer') for a in ans_list]
                if 'yes' in values and 'no' in values:
                    # Potential contradiction
                    yes_q = [a['question_id'] for a in ans_list if a.get('answer') == 'yes']
                    no_q = [a['question_id'] for a in ans_list if a.get('answer') == 'no']
                    for yq in yes_q:
                        for nq in no_q:
                            contradictions.append((yq, nq))
        
        return contradictions
    
    @staticmethod
    def calculate_answer_confidence(answers: List[Dict]) -> float:
        """
        Calculate overall confidence based on answer types
        
        Args:
            answers: List of answer dictionaries
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not answers:
            return 0.0
        
        # Map answers to confidence scores
        confidence_map = {
            'yes': 1.0,
            'no': 1.0,
            'probably': 0.7,
            'probably_not': 0.7,
            'dont_know': 0.0
        }
        
        total_confidence = sum(
            confidence_map.get(ans.get('answer', ''), 0.5)
            for ans in answers
        )
        
        return total_confidence / len(answers)
    
    @staticmethod
    def identify_key_characteristics(
        answers: List[Dict],
        min_confidence: float = 0.8
    ) -> Set[str]:
        """
        Identify characteristics that are confidently known
        
        Args:
            answers: List of answer dictionaries
            min_confidence: Minimum confidence threshold
            
        Returns:
            Set of characteristic names
        """
        key_chars = set()
        
        for ans in answers:
            answer_type = ans.get('answer', '')
            confidence = 0.0
            
            if answer_type in ['yes', 'no']:
                confidence = 1.0
            elif answer_type in ['probably', 'probably_not']:
                confidence = 0.7
            
            if confidence >= min_confidence:
                char = ans.get('characteristic')
                if char:
                    key_chars.add(char)
        
        return key_chars
    
    @staticmethod
    def suggest_clarifying_questions(
        answers: List[Dict],
        all_questions: List[Dict]
    ) -> List[Dict]:
        """
        Suggest questions that would clarify uncertain answers
        
        Args:
            answers: List of answer dictionaries
            all_questions: All available questions
            
        Returns:
            List of suggested question dictionaries
        """
        suggestions = []
        
        # Find characteristics with uncertain answers
        uncertain_chars = set()
        for ans in answers:
            if ans.get('answer') in ['dont_know', 'probably', 'probably_not']:
                char = ans.get('characteristic')
                if char:
                    uncertain_chars.add(char)
        
        # Find questions that clarify these characteristics
        for question in all_questions:
            if question.get('characteristic') in uncertain_chars:
                # Check if not already asked
                asked_ids = {a.get('question_id') for a in answers}
                if question.get('id') not in asked_ids:
                    suggestions.append(question)
        
        return suggestions[:5]  # Return top 5
    
    @staticmethod
    def analyze_answer_distribution(answers: List[Dict]) -> Dict[str, int]:
        """
        Analyze distribution of answer types
        
        Args:
            answers: List of answer dictionaries
            
        Returns:
            Dictionary mapping answer types to counts
        """
        answer_types = [ans.get('answer', 'unknown') for ans in answers]
        return dict(Counter(answer_types))
    
    @staticmethod
    def calculate_progress_score(
        answers: List[Dict],
        total_places: int,
        remaining_places: int
    ) -> float:
        """
        Calculate how much progress has been made
        
        Args:
            answers: List of answer dictionaries
            total_places: Total number of places at start
            remaining_places: Number of remaining possible places
            
        Returns:
            Progress score (0.0 to 1.0)
        """
        if total_places == 0:
            return 0.0
        
        # Progress based on elimination
        eliminated = total_places - remaining_places
        elimination_progress = eliminated / total_places
        
        # Progress based on questions asked (diminishing returns)
        question_progress = min(len(answers) / 20, 1.0)
        
        # Weighted average
        return 0.7 * elimination_progress + 0.3 * question_progress
    
    @staticmethod
    def estimate_questions_remaining(
        remaining_places: int,
        average_elimination_rate: float = 0.5
    ) -> int:
        """
        Estimate how many more questions are needed
        
        Args:
            remaining_places: Number of places still possible
            average_elimination_rate: Average fraction eliminated per question
            
        Returns:
            Estimated number of questions
        """
        if remaining_places <= 1:
            return 0
        
        if average_elimination_rate <= 0:
            return 10  # Default estimate
        
        # Use logarithmic estimate
        import math
        return max(1, int(math.log2(remaining_places) / math.log2(1 / (1 - average_elimination_rate))))