#include "../decision_tree.h"
#include <iostream>
#include <cassert>

using namespace guessmyplace;

void test_place_creation() {
    Place place("france", "France", "country");
    place.characteristics["continent"] = "europe";
    place.characteristics["population_millions"] = "67";
    
    assert(place.id == "france");
    assert(place.name == "France");
    assert(place.type == "country");
    assert(place.hasCharacteristic("continent"));
    assert(place.getCharacteristic("continent") == "europe");
    
    std::cout << "✓ Place creation test passed\n";
}

void test_question_matching() {
    Place place("france", "France", "country");
    place.characteristics["continent"] = "europe";
    
    Question question("q1", "Is it in Europe?", "continent", "europe");
    
    DecisionTree tree;
    auto filtered = tree.filterByAnswer({place}, question, "yes");
    
    assert(!filtered.empty());
    assert(filtered[0].id == "france");
    
    std::cout << "✓ Question matching test passed\n";
}

void test_information_gain() {
    // Create test places
    std::vector<Place> places;
    
    Place p1("france", "France", "country");
    p1.characteristics["continent"] = "europe";
    places.push_back(p1);
    
    Place p2("japan", "Japan", "country");
    p2.characteristics["continent"] = "asia";
    places.push_back(p2);
    
    Place p3("usa", "USA", "country");
    p3.characteristics["continent"] = "north_america";
    places.push_back(p3);
    
    // Create question
    Question question("q1", "Is it in Europe?", "continent", "europe");
    
    // Calculate information gain
    DecisionTree tree;
    double ig = tree.calculateInformationGain(question, places);
    
    assert(ig >= 0.0 && ig <= 1.0);
    std::cout << "✓ Information gain test passed (IG = " << ig << ")\n";
}

int main() {
    std::cout << "Running Decision Tree tests...\n\n";
    
    test_place_creation();
    test_question_matching();
    test_information_gain();
    
    std::cout << "\n✓ All tests passed!\n";
    return 0;
}