"""
Advanced question selection algorithms
"""

import math
from typing import List, Dict, Tuple, Optional
from collections import Counter


class QuestionSelector:
    """Advanced algorithms for selecting optimal questions"""
    
    @staticmethod
    def calculate_entropy(distribution: Dict[str, int]) -> float:
        """
        Calculate Shannon entropy of a distribution
        
        Args:
            distribution: Dictionary mapping categories to counts
            
        Returns:
            Entropy value (0.0 to log2(n))
        """
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in distribution.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        
        return entropy
    
    @staticmethod
    def calculate_gini_impurity(distribution: Dict[str, int]) -> float:
        """
        Calculate Gini impurity of a distribution
        
        Args:
            distribution: Dictionary mapping categories to counts
            
        Returns:
            Gini impurity (0.0 to 0.5)
        """
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        
        gini = 1.0
        for count in distribution.values():
            p = count / total
            gini -= p * p
        
        return gini
    
    @staticmethod
    def calculate_information_gain_ratio(
        parent_distribution: Dict[str, int],
        left_distribution: Dict[str, int],
        right_distribution: Dict[str, int]
    ) -> float:
        """
        Calculate information gain ratio (normalized information gain)
        
        Args:
            parent_distribution: Distribution before split
            left_distribution: Distribution in left subset
            right_distribution: Distribution in right subset
            
        Returns:
            Information gain ratio
        """
        # Calculate parent entropy
        parent_entropy = QuestionSelector.calculate_entropy(parent_distribution)
        
        # Calculate weighted child entropy
        total = sum(parent_distribution.values())
        if total == 0:
            return 0.0
        
        left_size = sum(left_distribution.values())
        right_size = sum(right_distribution.values())
        
        left_entropy = QuestionSelector.calculate_entropy(left_distribution)
        right_entropy = QuestionSelector.calculate_entropy(right_distribution)
        
        weighted_child_entropy = (
            (left_size / total) * left_entropy +
            (right_size / total) * right_entropy
        )
        
        # Information gain
        information_gain = parent_entropy - weighted_child_entropy
        
        # Split information (to normalize)
        split_info = 0.0
        if left_size > 0:
            p_left = left_size / total
            split_info -= p_left * math.log2(p_left)
        if right_size > 0:
            p_right = right_size / total
            split_info -= p_right * math.log2(p_right)
        
        # Gain ratio
        if split_info > 0:
            return information_gain / split_info
        else:
            return information_gain
    
    @staticmethod
    def select_by_variance_reduction(
        places: List[Dict],
        questions: List[Dict],
        characteristic: str = 'type'
    ) -> Optional[Dict]:
        """
        Select question that maximizes variance reduction
        
        Args:
            places: List of place dictionaries
            questions: List of available questions
            characteristic: Characteristic to measure variance on
            
        Returns:
            Best question, or None
        """
        if not places or not questions:
            return None
        
        # Calculate variance of current set
        values = [p.get(characteristic) for p in places if characteristic in p]
        if not values:
            return None
        
        # For categorical data, use entropy as "variance"
        value_counts = Counter(values)
        parent_variance = QuestionSelector.calculate_entropy(value_counts)
        
        best_question = None
        best_reduction = -1.0
        
        for question in questions:
            # Simulate split
            left = []
            right = []
            
            for place in places:
                # Simplified: assume binary split
                if QuestionSelector._matches_question(place, question):
                    left.append(place)
                else:
                    right.append(place)
            
            # Calculate variance of subsets
            left_values = [p.get(characteristic) for p in left if characteristic in p]
            right_values = [p.get(characteristic) for p in right if characteristic in p]
            
            left_variance = QuestionSelector.calculate_entropy(Counter(left_values)) if left_values else 0.0
            right_variance = QuestionSelector.calculate_entropy(Counter(right_values)) if right_values else 0.0
            
            # Weighted variance
            total = len(places)
            weighted_variance = (
                (len(left) / total) * left_variance +
                (len(right) / total) * right_variance
            )
            
            # Variance reduction
            reduction = parent_variance - weighted_variance
            
            if reduction > best_reduction:
                best_reduction = reduction
                best_question = question
        
        return best_question
    
    @staticmethod
    def _matches_question(place: Dict, question: Dict) -> bool:
        """Helper to check if place matches question"""
        char = question.get('characteristic')
        value = question.get('value')
        operator = question.get('operator', 'equals')
        
        if char not in place.get('characteristics', {}):
            return False
        
        place_value = place['characteristics'][char]
        
        if operator == 'equals':
            return place_value == value
        elif operator == 'not_equals':
            return place_value != value
        elif operator == 'greater_than':
            try:
                return float(place_value) > float(value)
            except:
                return False
        elif operator == 'less_than':
            try:
                return float(place_value) < float(value)
            except:
                return False
        elif operator == 'contains':
            return value in str(place_value)
        
        return False