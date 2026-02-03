#!/bin/bash

# GuessMyPlace - Test Runner Script
# Runs all tests across backend, frontend, and C++

set -e

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
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Track test results
BACKEND_TESTS_PASSED=0
FRONTEND_TESTS_PASSED=0
CPP_TESTS_PASSED=0
DATA_VALIDATION_PASSED=0

# Test backend
test_backend() {
    print_header "Running Backend Tests"
    
    cd backend
    
    if [ -d "venv" ]; then
        source venv/bin/activate || . venv/Scripts/activate
    fi
    
    # Unit tests
    print_info "Running Python unit tests..."
    if pytest tests/unit/ -v --cov=app --cov-report=term-missing; then
        print_success "Backend unit tests passed"
    else
        print_error "Backend unit tests failed"
        cd ..
        return 1
    fi
    
    # Integration tests
    if [ -d "tests/integration" ] && [ "$(ls -A tests/integration)" ]; then
        print_info "Running integration tests..."
        if pytest tests/integration/ -v; then
            print_success "Integration tests passed"
        else
            print_error "Integration tests failed"
            cd ..
            return 1
        fi
    fi
    
    # Linting
    print_info "Running flake8..."
    if flake8 app/ --max-line-length=88 --extend-ignore=E203; then
        print_success "Linting passed"
    else
        print_error "Linting failed"
        cd ..
        return 1
    fi
    
    # Type checking
    if command -v mypy >/dev/null 2>&1; then
        print_info "Running mypy..."
        if mypy app/ --ignore-missing-imports; then
            print_success "Type checking passed"
        else
            print_error "Type checking failed"
            cd ..
            return 1
        fi
    fi
    
    cd ..
    BACKEND_TESTS_PASSED=1
    return 0
}

# Test frontend
test_frontend() {
    print_header "Running Frontend Tests"
    
    cd frontend
    
    # Unit tests
    print_info "Running frontend tests..."
    if npm test -- --run; then
        print_success "Frontend tests passed"
    else
        print_error "Frontend tests failed"
        cd ..
        return 1
    fi
    
    # Linting
    print_info "Running ESLint..."
    if npm run lint; then
        print_success "Frontend linting passed"
    else
        print_error "Frontend linting failed"
        cd ..
        return 1
    fi
    
    # Type checking
    print_info "Running TypeScript check..."
    if npm run type-check; then
        print_success "Type checking passed"
    else
        print_error "Type checking failed"
        cd ..
        return 1
    fi
    
    # Build test
    print_info "Testing production build..."
    if npm run build; then
        print_success "Build successful"
        rm -rf dist
    else
        print_error "Build failed"
        cd ..
        return 1
    fi
    
    cd ..
    FRONTEND_TESTS_PASSED=1
    return 0
}

# Test C++ modules
test_cpp() {
    print_header "Running C++ Tests"
    
    if [ ! -d "backend/algorithms/cpp/build" ]; then
        print_info "C++ modules not built, skipping tests"
        return 0
    fi
    
    cd backend/algorithms/cpp/build
    
    print_info "Running C++ unit tests..."
    if ctest --output-on-failure; then
        print_success "C++ tests passed"
        cd ../../../..
        CPP_TESTS_PASSED=1
        return 0
    else
        print_error "C++ tests failed"
        cd ../../../..
        return 1
    fi
}

# Validate data
validate_data() {
    print_header "Validating Data Files"
    
    if [ -f "data/scripts/validate_data.py" ]; then
        print_info "Running data validation..."
        if python data/scripts/validate_data.py; then
            print_success "Data validation passed"
            DATA_VALIDATION_PASSED=1
            return 0
        else
            print_error "Data validation failed"
            return 1
        fi
    else
        print_info "Data validation script not found, skipping"
        return 0
    fi
}

# Run all tests
run_all_tests() {
    local start_time=$(date +%s)
    
    print_header "GuessMyPlace - Test Suite"
    
    # Data validation (fast, run first)
    validate_data || true
    
    # Backend tests
    test_backend || true
    
    # Frontend tests
    test_frontend || true
    
    # C++ tests
    test_cpp || true
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Summary
    print_header "Test Summary"
    
    echo "Test Results:"
    echo ""
    
    if [ $DATA_VALIDATION_PASSED -eq 1 ]; then
        echo -e "  ${GREEN}✓${NC} Data Validation"
    else
        echo -e "  ${RED}✗${NC} Data Validation"
    fi
    
    if [ $BACKEND_TESTS_PASSED -eq 1 ]; then
        echo -e "  ${GREEN}✓${NC} Backend Tests"
    else
        echo -e "  ${RED}✗${NC} Backend Tests"
    fi
    
    if [ $FRONTEND_TESTS_PASSED -eq 1 ]; then
        echo -e "  ${GREEN}✓${NC} Frontend Tests"
    else
        echo -e "  ${RED}✗${NC} Frontend Tests"
    fi
    
    if [ $CPP_TESTS_PASSED -eq 1 ]; then
        echo -e "  ${GREEN}✓${NC} C++ Tests"
    else
        echo -e "  ${YELLOW}○${NC} C++ Tests (skipped or not built)"
    fi
    
    echo ""
    echo "Duration: ${duration}s"
    echo ""
    
    # Exit with error if any tests failed
    if [ $BACKEND_TESTS_PASSED -eq 0 ] || [ $FRONTEND_TESTS_PASSED -eq 0 ] || [ $DATA_VALIDATION_PASSED -eq 0 ]; then
        print_error "Some tests failed"
        exit 1
    else
        print_success "All tests passed! 🎉"
        exit 0
    fi
}

# Parse command line arguments
case "${1:-all}" in
    backend)
        test_backend
        ;;
    frontend)
        test_frontend
        ;;
    cpp)
        test_cpp
        ;;
    data)
        validate_data
        ;;
    all)
        run_all_tests
        ;;
    *)
        echo "Usage: $0 [backend|frontend|cpp|data|all]"
        echo ""
        echo "Examples:"
        echo "  $0           # Run all tests"
        echo "  $0 all       # Run all tests"
        echo "  $0 backend   # Run only backend tests"
        echo "  $0 frontend  # Run only frontend tests"
        echo "  $0 cpp       # Run only C++ tests"
        echo "  $0 data      # Run only data validation"
        exit 1
        ;;
esac