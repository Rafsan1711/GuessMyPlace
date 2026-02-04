#ifndef INFORMATION_GAIN_H
#define INFORMATION_GAIN_H

#include <vector>
#include <map>
#include <string>

namespace guessmyplace {

/**
 * @brief Calculator for information gain metrics
 */
class InformationGainCalculator {
public:
    /**
     * @brief Calculate entropy for a distribution
     * 
     * @param distribution Map of categories to counts
     * @return Entropy value
     */
    static double calculateEntropy(const std::map<std::string, int>& distribution);
    
    /**
     * @brief Calculate information gain for a split
     * 
     * @param parent_entropy Entropy of parent set
     * @param left_size Size of left subset
     * @param left_entropy Entropy of left subset
     * @param right_size Size of right subset
     * @param right_entropy Entropy of right subset
     * @return Information gain value
     */
    static double calculateInformationGain(
        double parent_entropy,
        int left_size,
        double left_entropy,
        int right_size,
        double right_entropy
    );
    
    /**
     * @brief Calculate Gini impurity
     * 
     * @param distribution Map of categories to counts
     * @return Gini impurity value
     */
    static double calculateGiniImpurity(const std::map<std::string, int>& distribution);
};

} // namespace guessmyplace

#endif // INFORMATION_GAIN_H