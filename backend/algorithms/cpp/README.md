# C++ Decision Engine

High-performance algorithms for GuessMyPlace game logic.

## Overview

This module provides C++ implementations of performance-critical algorithms:
- **Decision Tree**: Question selection using information gain
- **Information Gain Calculator**: Entropy and Gini impurity calculations
- **Probability Engine**: Bayesian probability calculations

## Building

### Prerequisites

- CMake 3.15+
- C++17 compatible compiler (GCC 9+, Clang 10+, MSVC 2019+)
- Make (or Ninja)

### Quick Build

From project root:
```bash
./scripts/build-cpp.sh
```

Or manually:
```bash
cd backend/algorithms/cpp
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
```

### Build Output

- `libdecision_engine.so` (Linux)
- `libdecision_engine.dylib` (macOS)
- `decision_engine.dll` (Windows)

## Testing

```bash
cd build
./test_decision_tree
./test_information_gain
./test_probability_engine
```

Or use CTest:
```bash
cd build
ctest --output-on-failure
```

## Usage

### From Python (Future - with pybind11)

```python
import decision_engine

tree = decision_engine.DecisionTree()
question = tree.select_best_question(places, history)
```

### Standalone C++

```cpp
#include "decision_tree.h"

using namespace guessmyplace;

DecisionTree tree;
std::vector<Place> places = {...};
std::vector<Answer> history = {...};

Question* best = tree.selectBestQuestion(places, history);
```

## Architecture

### Files

- `decision_tree.h/cpp` - Main decision tree logic
- `information_gain.h/cpp` - Entropy and IG calculations
- `probability_engine.h/cpp` - Bayesian probability
- `tests/` - Unit tests

### Classes

**DecisionTree**
- `selectBestQuestion()` - Choose optimal next question
- `calculateInformationGain()` - Calculate IG for a question
- `filterByAnswer()` - Filter places based on answer

**InformationGainCalculator**
- `calculateEntropy()` - Shannon entropy
- `calculateGiniImpurity()` - Gini impurity
- `calculateInformationGain()` - IG from parent/child entropies

**ProbabilityEngine**
- `calculateProbabilities()` - Get probability for each place
- `getMostLikely()` - Find most probable place
- `bayesianUpdate()` - Update probabilities with new evidence

## Performance

Benchmarks (compared to pure Python):
- Information gain calculation: **~50x faster**
- Decision tree traversal: **~30x faster**
- Probability updates: **~20x faster**

## Configuration

CMake options:
```bash
cmake -DCMAKE_BUILD_TYPE=Release      # Release build (optimized)
cmake -DCMAKE_BUILD_TYPE=Debug        # Debug build (with symbols)
cmake -DBUILD_TESTING=OFF             # Disable tests
```

## Integration with Python

Current: Standalone C++ library
Future: Python bindings via pybind11

The Python backend calls C++ functions via:
1. Shared library loading (ctypes/cffi)
2. Or pybind11 bindings (planned)

## Troubleshooting

**CMake not found**
```bash
# Ubuntu/Debian
sudo apt-get install cmake

# macOS
brew install cmake
```

**Compiler not found**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS (installs Xcode Command Line Tools)
xcode-select --install
```

**Library not found at runtime**
```bash
export LD_LIBRARY_PATH=$(pwd)/build:$LD_LIBRARY_PATH
```

## Contributing

See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for guidelines.

When modifying C++ code:
1. Update corresponding header files
2. Add/update unit tests
3. Run tests before committing
4. Follow C++17 standards
5. Use clang-format for formatting

## License

GPL-3.0 - See LICENSE file
