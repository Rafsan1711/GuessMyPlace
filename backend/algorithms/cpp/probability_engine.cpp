#include "probability_engine.h"
#include <algorithm>
#include <cmath>

namespace guessmyplace {

ProbabilityEngine::ProbabilityEngine() {
    // Initialize with uniform priors
}

ProbabilityEngine::~ProbabilityEngine() {
    // Destructor
}

std::map<std::string, double> ProbabilityEngine::calculateProbabilities(
    const std::vector<Place>& places,
    const std::vector<Answer>& answers
) {
    std::map<std::string, double> probabilities;
    
    if (places.empty()) {
        return probabilities;
    }
    
    // Start with uniform prior
    double uniform_prior = 1.0 / places.size();
    
    // Calculate likelihood for each place
    std::vector<double> likelihoods;
    double total_likelihood = 0.0;
    
    for (const auto& place : places) {
        double likelihood = calculateLikelihood(place, answers);
        likelihoods.push_back(likelihood);
        total_likelihood += likelihood;
    }
    
    // Normalize to get probabilities
    for (size_t i = 0; i < places.size(); ++i) {
        double prob = (total_likelihood > 0.0) 
            ? likelihoods[i] / total_likelihood
            : uniform_prior;
        
        probabilities[places[i].id] = prob;
    }
    
    return probabilities;
}

std::string ProbabilityEngine::getMostLikely(
    const std::map<std::string, double>& probabilities
) {
    if (probabilities.empty()) {
        return "";
    }
    
    // Find place with highest probability
    std::string best_place;
    double best_prob = -1.0;
    
    for (const auto& pair : probabilities) {
        if (pair.second > best_prob) {
            best_prob = pair.second;
            best_place = pair.first;
        }
    }
    
    return best_place;
}

double ProbabilityEngine::bayesianUpdate(
    double prior,
    double likelihood,
    double evidence
) {
    if (evidence == 0.0) {
        return prior;
    }
    
    // Bayes' theorem: P(H|E) = P(E|H) * P(H) / P(E)
    return (likelihood * prior) / evidence;
}

double ProbabilityEngine::calculateLikelihood(
    const Place& place,
    const std::vector<Answer>& answers
) {
    if (answers.empty()) {
        return 1.0;
    }
    
    // Simple likelihood: product of match probabilities
    double likelihood = 1.0;
    
    for (const auto& answer : answers) {
        // TODO: Implement proper likelihood calculation
        // For now, use simple binary match
        // This should be improved with actual question data
        
        // Assign higher likelihood if answer is consistent with place
        if (answer.answer == "yes") {
            likelihood *= 0.9;  // High confidence match
        } else if (answer.answer == "no") {
            likelihood *= 0.9;  // High confidence non-match
        } else if (answer.answer == "probably") {
            likelihood *= 0.7;  // Medium confidence match
        } else if (answer.answer == "probably_not") {
            likelihood *= 0.7;  // Medium confidence non-match
        } else if (answer.answer == "dont_know") {
            likelihood *= 0.5;  // No information
        }
    }
    
    return likelihood;
}

} // namespace guessmyplace