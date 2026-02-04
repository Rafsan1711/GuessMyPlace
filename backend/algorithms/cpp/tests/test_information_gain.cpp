#include "../information_gain.h"
#include <iostream>
#include <cassert>
#include <cmath>

using namespace guessmyplace;

void test_entropy_calculation() {
    std::map<std::string, int> distribution;
    
    // Uniform distribution (max entropy)
    distribution["A"] = 1;
    distribution["B"] = 1;
    distribution["C"] = 1;
    distribution["D"] = 1;
    
    double entropy = InformationGainCalculator::calculateEntropy(distribution);
    
    // Expected: log2(4) = 2.0
    assert(std::abs(entropy - 2.0) < 0.001);
    
    std::cout << "✓ Entropy calculation test passed (uniform dist = " << entropy << ")\n";
}

void test_entropy_pure() {
    std::map<std::string, int> distribution;
    
    // Pure distribution (zero entropy)
    distribution["A"] = 10;
    
    double entropy = InformationGainCalculator::calculateEntropy(distribution);
    
    // Expected: 0.0
    assert(std::abs(entropy) < 0.001);
    
    std::cout << "✓ Pure distribution entropy test passed (entropy = " << entropy << ")\n";
}

void test_information_gain() {
    // Parent entropy
    std::map<std::string, int> parent;
    parent["type1"] = 5;
    parent["type2"] = 5;
    
    double parent_entropy = InformationGainCalculator::calculateEntropy(parent);
    
    // Left child (pure)
    std::map<std::string, int> left;
    left["type1"] = 5;
    double left_entropy = InformationGainCalculator::calculateEntropy(left);
    
    // Right child (pure)
    std::map<std::string, int> right;
    right["type2"] = 5;
    double right_entropy = InformationGainCalculator::calculateEntropy(right);
    
    // Calculate information gain
    double ig = InformationGainCalculator::calculateInformationGain(
        parent_entropy, 5, left_entropy, 5, right_entropy
    );
    
    // Perfect split should give IG = parent_entropy
    assert(std::abs(ig - parent_entropy) < 0.001);
    
    std::cout << "✓ Information gain test passed (IG = " << ig << ")\n";
}

void test_gini_impurity() {
    std::map<std::string, int> distribution;
    
    // Pure distribution
    distribution["A"] = 10;
    double gini_pure = InformationGainCalculator::calculateGiniImpurity(distribution);
    assert(std::abs(gini_pure) < 0.001);
    
    // 50-50 split
    distribution.clear();
    distribution["A"] = 5;
    distribution["B"] = 5;
    double gini_split = InformationGainCalculator::calculateGiniImpurity(distribution);
    assert(std::abs(gini_split - 0.5) < 0.001);
    
    std::cout << "✓ Gini impurity test passed\n";
}

int main() {
    std::cout << "Running Information Gain tests...\n\n";
    
    test_entropy_calculation();
    test_entropy_pure();
    test_information_gain();
    test_gini_impurity();
    
    std::cout << "\n✓ All Information Gain tests passed!\n";
    return 0;
}