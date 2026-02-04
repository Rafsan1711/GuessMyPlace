#ifndef PROBABILITY_ENGINE_H
#define PROBABILITY_ENGINE_H

#include "decision_tree.h"
#include <map>
#include <vector>

namespace guessmyplace {

/**
 * @brief Engine for calculating place probabilities
 */
class ProbabilityEngine {
public:
    ProbabilityEngine();
    ~ProbabilityEngine();
    
    /**
     * @brief Calculate probabilities for each place
     * 
     * @param places Vector of possible places
     * @param answers Vector of question answers
     * @return Map of place ID to probability
     */
    std::map<std::string, double> calculateProbabilities(
        const std::vector<Place>& places,
        const std::vector<Answer>& answers
    );
    
    /**
     * @brief Get the most likely place
     * 
     * @param probabilities Map of place probabilities
     * @return ID of most likely place
     */
    std::string getMostLikely(const std::map<std::string, double>& probabilities);
    
    /**
     * @brief Update probability using Bayesian inference
     * 
     * @param prior Prior probability
     * @param likelihood Likelihood of evidence
     * @param evidence Total evidence probability
     * @return Updated posterior probability
     */
    double bayesianUpdate(double prior, double likelihood, double evidence);

private:
    /**
     * @brief Calculate likelihood for a place given answers
     * 
     * @param place The place to evaluate
     * @param answers Vector of answers
     * @return Likelihood score
     */
    double calculateLikelihood(
        const Place& place,
        const std::vector<Answer>& answers
    );
    
    // Prior probabilities (can be adjusted based on popularity)
    std::map<std::string, double> priors_;
};

} // namespace guessmyplace

#endif // PROBABILITY_ENGINE_H