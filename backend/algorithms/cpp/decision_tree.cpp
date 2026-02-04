#include "decision_tree.h"
#include "information_gain.h"
#include <cmath>
#include <algorithm>
#include <limits>

namespace guessmyplace {

// Place methods
bool Place::hasCharacteristic(const std::string& key) const {
    return characteristics.find(key) != characteristics.end();
}

std::string Place::getCharacteristic(const std::string& key) const {
    auto it = characteristics.find(key);
    return (it != characteristics.end()) ? it->second : "";
}

// DecisionTree implementation
DecisionTree::DecisionTree() {
    // Constructor
}

DecisionTree::~DecisionTree() {
    // Destructor
}

Question* DecisionTree::selectBestQuestion(
    const std::vector<Place>& places,
    const std::vector<Answer>& history
) {
    if (places.empty()) {
        return nullptr;
    }
    
    // Get list of already asked questions
    std::vector<std::string> asked_ids;
    for (const auto& ans : history) {
        asked_ids.push_back(ans.question_id);
    }
    
    // Find best question from available questions
    double best_score = -1.0;
    Question* best_question = nullptr;
    
    for (auto& question : available_questions_) {
        // Skip if already asked
        bool already_asked = false;
        for (const auto& id : asked_ids) {
            if (question.id == id) {
                already_asked = true;
                break;
            }
        }
        if (already_asked) continue;
        
        // Calculate information gain
        double ig = calculateInformationGain(question, places);
        
        // Weight by discriminating power
        double score = ig * question.discriminating_power;
        
        if (score > best_score) {
            best_score = score;
            best_question = &question;
        }
    }
    
    return best_question;
}

double DecisionTree::calculateInformationGain(
    const Question& question,
    const std::vector<Place>& places
) {
    if (places.empty()) {
        return 0.0;
    }
    
    // Count places that would answer "yes" vs "no"
    int yes_count = 0;
    int no_count = 0;
    
    for (const auto& place : places) {
        if (placeMatchesQuestion(place, question, "yes")) {
            yes_count++;
        } else {
            no_count++;
        }
    }
    
    // Calculate information gain using entropy
    double total = static_cast<double>(places.size());
    double yes_ratio = yes_count / total;
    double no_ratio = no_count / total;
    
    // Entropy formula: -p*log2(p)
    auto entropy = [](double p) -> double {
        if (p <= 0.0 || p >= 1.0) return 0.0;
        return -p * std::log2(p);
    };
    
    double information_gain = entropy(yes_ratio) + entropy(no_ratio);
    
    return information_gain;
}

std::vector<Place> DecisionTree::filterByAnswer(
    const std::vector<Place>& places,
    const Question& question,
    const std::string& answer
) {
    std::vector<Place> filtered;
    
    for (const auto& place : places) {
        if (placeMatchesQuestion(place, question, answer)) {
            filtered.push_back(place);
        }
    }
    
    // If no places match, return original list
    return filtered.empty() ? places : filtered;
}

double DecisionTree::calculateEntropy(const std::vector<Place>& places) {
    if (places.empty()) {
        return 0.0;
    }
    
    // For simplicity, calculate entropy based on place types
    std::map<std::string, int> type_counts;
    
    for (const auto& place : places) {
        type_counts[place.type]++;
    }
    
    double entropy = 0.0;
    double total = static_cast<double>(places.size());
    
    for (const auto& pair : type_counts) {
        double p = pair.second / total;
        if (p > 0.0) {
            entropy -= p * std::log2(p);
        }
    }
    
    return entropy;
}

bool DecisionTree::placeMatchesQuestion(
    const Place& place,
    const Question& question,
    const std::string& answer
) {
    // Get the characteristic value from the place
    if (!place.hasCharacteristic(question.characteristic)) {
        return (answer == "dont_know");
    }
    
    std::string place_value = place.getCharacteristic(question.characteristic);
    
    // Determine if place matches based on operator
    bool matches = false;
    
    if (question.op == "equals") {
        matches = (place_value == question.value);
    } else if (question.op == "not_equals") {
        matches = (place_value != question.value);
    } else if (question.op == "greater_than") {
        try {
            double pv = std::stod(place_value);
            double qv = std::stod(question.value);
            matches = (pv > qv);
        } catch (...) {
            matches = false;
        }
    } else if (question.op == "less_than") {
        try {
            double pv = std::stod(place_value);
            double qv = std::stod(question.value);
            matches = (pv < qv);
        } catch (...) {
            matches = false;
        }
    } else if (question.op == "contains") {
        matches = (place_value.find(question.value) != std::string::npos);
    }
    
    // Map answer to boolean result
    if (answer == "yes") {
        return matches;
    } else if (answer == "no") {
        return !matches;
    } else if (answer == "probably") {
        return matches;
    } else if (answer == "probably_not") {
        return !matches;
    } else if (answer == "dont_know") {
        return true;  // Keep all places
    }
    
    return true;
}

} // namespace guessmyplace