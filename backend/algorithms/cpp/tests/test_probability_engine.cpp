#include "../probability_engine.h"
#include <iostream>
#include <cassert>
#include <cmath>

using namespace guessmyplace;

void test_probability_calculation() {
    ProbabilityEngine engine;
    
    // Create test places
    std::vector<Place> places;
    places.emplace_back("france", "France", "country");
    places.emplace_back("japan", "Japan", "country");
    places.emplace_back("usa", "USA", "country");
    
    // Empty answer history
    std::vector<Answer> answers;
    
    // Calculate probabilities
    auto probs = engine.calculateProbabilities(places, answers);
    
    // Should have uniform distribution
    assert(probs.size() == 3);
    
    double sum = 0.0;
    for (const auto& pair : probs) {
        sum += pair.second;
        // Each probability should be around 1/3
        assert(pair.second > 0.2 && pair.second < 0.4);
    }
    
    // Probabilities should sum to ~1.0
    assert(std::abs(sum - 1.0) < 0.01);
    
    std::cout << "✓ Probability calculation test passed\n";
}

void test_most_likely_place() {
    ProbabilityEngine engine;
    
    std::map<std::string, double> probs;
    probs["france"] = 0.1;
    probs["japan"] = 0.7;
    probs["usa"] = 0.2;
    
    std::string most_likely = engine.getMostLikely(probs);
    
    assert(most_likely == "japan");
    
    std::cout << "✓ Most likely place test passed (selected: " << most_likely << ")\n";
}

void test_bayesian_update() {
    ProbabilityEngine engine;
    
    double prior = 0.5;
    double likelihood = 0.8;
    double evidence = 0.6;
    
    double posterior = engine.bayesianUpdate(prior, likelihood, evidence);
    
    // P(H|E) = P(E|H) * P(H) / P(E) = 0.8 * 0.5 / 0.6 = 0.667
    double expected = (likelihood * prior) / evidence;
    
    assert(std::abs(posterior - expected) < 0.001);
    
    std::cout << "✓ Bayesian update test passed (posterior = " << posterior << ")\n";
}

void test_empty_places() {
    ProbabilityEngine engine;
    
    std::vector<Place> places;
    std::vector<Answer> answers;
    
    auto probs = engine.calculateProbabilities(places, answers);
    
    assert(probs.empty());
    
    std::cout << "✓ Empty places test passed\n";
}

int main() {
    std::cout << "Running Probability Engine tests...\n\n";
    
    test_probability_calculation();
    test_most_likely_place();
    test_bayesian_update();
    test_empty_places();
    
    std::cout << "\n✓ All Probability Engine tests passed!\n";
    return 0;
}