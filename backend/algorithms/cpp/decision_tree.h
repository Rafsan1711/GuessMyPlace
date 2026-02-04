#ifndef DECISION_TREE_H
#define DECISION_TREE_H

#include <string>
#include <vector>
#include <map>
#include <memory>

namespace guessmyplace {

// Forward declarations
struct Place;
struct Question;
struct Answer;

/**
 * @brief Represents a place in the game
 */
struct Place {
    std::string id;
    std::string name;
    std::string type;
    std::map<std::string, std::string> characteristics;
    
    Place(const std::string& id, const std::string& name, const std::string& type)
        : id(id), name(name), type(type) {}
    
    bool hasCharacteristic(const std::string& key) const;
    std::string getCharacteristic(const std::string& key) const;
};

/**
 * @brief Represents a question
 */
struct Question {
    std::string id;
    std::string text;
    std::string characteristic;
    std::string value;
    std::string op;  // operator: equals, greater_than, etc.
    double discriminating_power;
    
    Question(const std::string& id, const std::string& text,
             const std::string& characteristic, const std::string& value)
        : id(id), text(text), characteristic(characteristic), 
          value(value), op("equals"), discriminating_power(0.5) {}
};

/**
 * @brief Represents an answer to a question
 */
struct Answer {
    std::string question_id;
    std::string answer;  // yes, no, probably, etc.
    
    Answer(const std::string& qid, const std::string& ans)
        : question_id(qid), answer(ans) {}
};

/**
 * @brief Decision tree for selecting optimal questions
 */
class DecisionTree {
public:
    DecisionTree();
    ~DecisionTree();
    
    /**
     * @brief Select the best question to ask next
     * 
     * @param places Vector of currently possible places
     * @param history Vector of previously asked questions and answers
     * @return Best question to ask, or nullptr if no suitable question
     */
    Question* selectBestQuestion(
        const std::vector<Place>& places,
        const std::vector<Answer>& history
    );
    
    /**
     * @brief Calculate information gain for a question
     * 
     * @param question The question to evaluate
     * @param places Vector of places
     * @return Information gain value (0.0 to 1.0)
     */
    double calculateInformationGain(
        const Question& question,
        const std::vector<Place>& places
    );
    
    /**
     * @brief Filter places based on an answer
     * 
     * @param places Vector of places to filter
     * @param question The question that was asked
     * @param answer The answer given
     * @return Filtered vector of places
     */
    std::vector<Place> filterByAnswer(
        const std::vector<Place>& places,
        const Question& question,
        const std::string& answer
    );

private:
    /**
     * @brief Calculate entropy of a set of places
     * 
     * @param places Vector of places
     * @return Entropy value
     */
    double calculateEntropy(const std::vector<Place>& places);
    
    /**
     * @brief Check if a place matches a question based on answer
     * 
     * @param place The place to check
     * @param question The question
     * @param answer The answer
     * @return true if place matches, false otherwise
     */
    bool placeMatchesQuestion(
        const Place& place,
        const Question& question,
        const std::string& answer
    );
    
    // Private members
    std::vector<Question> available_questions_;
};

} // namespace guessmyplace

#endif // DECISION_TREE_H