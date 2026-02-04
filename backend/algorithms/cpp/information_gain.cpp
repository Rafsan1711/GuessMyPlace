#include "information_gain.h"
#include <cmath>

namespace guessmyplace {

double InformationGainCalculator::calculateEntropy(
    const std::map<std::string, int>& distribution
) {
    if (distribution.empty()) {
        return 0.0;
    }
    
    // Calculate total count
    int total = 0;
    for (const auto& pair : distribution) {
        total += pair.second;
    }
    
    if (total == 0) {
        return 0.0;
    }
    
    // Calculate entropy: -sum(p * log2(p))
    double entropy = 0.0;
    
    for (const auto& pair : distribution) {
        double probability = static_cast<double>(pair.second) / total;
        if (probability > 0.0) {
            entropy -= probability * std::log2(probability);
        }
    }
    
    return entropy;
}

double InformationGainCalculator::calculateInformationGain(
    double parent_entropy,
    int left_size,
    double left_entropy,
    int right_size,
    double right_entropy
) {
    int total = left_size + right_size;
    
    if (total == 0) {
        return 0.0;
    }
    
    // Weighted average of child entropies
    double weighted_child_entropy = 
        (static_cast<double>(left_size) / total) * left_entropy +
        (static_cast<double>(right_size) / total) * right_entropy;
    
    // Information gain = parent entropy - weighted child entropy
    return parent_entropy - weighted_child_entropy;
}

double InformationGainCalculator::calculateGiniImpurity(
    const std::map<std::string, int>& distribution
) {
    if (distribution.empty()) {
        return 0.0;
    }
    
    // Calculate total count
    int total = 0;
    for (const auto& pair : distribution) {
        total += pair.second;
    }
    
    if (total == 0) {
        return 0.0;
    }
    
    // Calculate Gini impurity: 1 - sum(p^2)
    double gini = 1.0;
    
    for (const auto& pair : distribution) {
        double probability = static_cast<double>(pair.second) / total;
        gini -= probability * probability;
    }
    
    return gini;
}

} // namespace guessmyplace