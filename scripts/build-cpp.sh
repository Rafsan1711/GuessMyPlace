#!/bin/bash

# Build C++ modules script
# Builds the C++ decision engine with proper error handling

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "backend/algorithms/cpp" ]; then
    print_error "Must run from project root directory"
    exit 1
fi

print_header "Building C++ Decision Engine"

# Navigate to C++ directory
cd backend/algorithms/cpp

# Check for required tools
print_info "Checking build tools..."

if ! command -v cmake &> /dev/null; then
    print_error "CMake not found. Please install CMake 3.15+"
    exit 1
fi
print_success "CMake found: $(cmake --version | head -n1)"

if ! command -v make &> /dev/null; then
    print_error "Make not found. Please install make"
    exit 1
fi
print_success "Make found"

if ! command -v g++ &> /dev/null && ! command -v clang++ &> /dev/null; then
    print_error "C++ compiler not found. Please install g++ or clang++"
    exit 1
fi
if command -v g++ &> /dev/null; then
    print_success "g++ found: $(g++ --version | head -n1)"
elif command -v clang++ &> /dev/null; then
    print_success "clang++ found: $(clang++ --version | head -n1)"
fi

# Clean previous build
print_info "Cleaning previous build..."
rm -rf build
mkdir -p build
print_success "Build directory created"

# Run CMake
print_info "Running CMake configuration..."
cd build

if cmake -DCMAKE_BUILD_TYPE=Release ..; then
    print_success "CMake configuration successful"
else
    print_error "CMake configuration failed"
    exit 1
fi

# Build
print_info "Building C++ modules..."
if make -j$(nproc 2>/dev/null || echo 2); then
    print_success "Build successful"
else
    print_error "Build failed"
    exit 1
fi

# Verify build artifacts
print_header "Verifying Build Artifacts"

print_info "Listing build directory contents:"
ls -lh

# Check for shared library
if [ -f "libdecision_engine.so" ]; then
    print_success "Found libdecision_engine.so"
    print_info "Size: $(ls -lh libdecision_engine.so | awk '{print $5}')"
elif [ -f "libdecision_engine.dylib" ]; then
    print_success "Found libdecision_engine.dylib (macOS)"
    print_info "Size: $(ls -lh libdecision_engine.dylib | awk '{print $5}')"
elif [ -f "decision_engine.dll" ]; then
    print_success "Found decision_engine.dll (Windows)"
else
    print_warning "Shared library not found, checking for static library..."
    if [ -f "libdecision_engine.a" ]; then
        print_success "Found libdecision_engine.a (static library)"
    else
        print_error "No library files found!"
        exit 1
    fi
fi

# Run tests if available
if [ -f "test_decision_tree" ]; then
    print_header "Running Tests"
    
    print_info "Running decision tree tests..."
    if ./test_decision_tree; then
        print_success "Decision tree tests passed"
    else
        print_warning "Decision tree tests failed"
    fi
    
    if [ -f "test_information_gain" ]; then
        print_info "Running information gain tests..."
        ./test_information_gain || print_warning "Information gain tests failed"
    fi
    
    if [ -f "test_probability_engine" ]; then
        print_info "Running probability engine tests..."
        ./test_probability_engine || print_warning "Probability engine tests failed"
    fi
else
    print_warning "Test executables not found"
fi

# Print summary
print_header "Build Summary"
print_success "C++ modules built successfully!"
print_info "Build artifacts located in: backend/algorithms/cpp/build/"
print_info "To use in Python, set LD_LIBRARY_PATH or copy .so to system lib directory"

echo ""
print_info "Next steps:"
echo "  1. Test the library: ./test_decision_tree"
echo "  2. Install system-wide: sudo make install"
echo "  3. Or add to LD_LIBRARY_PATH: export LD_LIBRARY_PATH=\$(pwd):\$LD_LIBRARY_PATH"
echo ""
