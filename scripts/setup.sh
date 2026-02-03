#!/bin/bash

# GuessMyPlace - Development Environment Setup Script
# This script sets up the complete development environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local missing_deps=()
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js not found"
        missing_deps+=("Node.js 18+")
    fi
    
    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python3 not found"
        missing_deps+=("Python 3.10+")
    fi
    
    # Check Docker
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker found: $DOCKER_VERSION"
    else
        print_error "Docker not found"
        missing_deps+=("Docker")
    fi
    
    # Check Docker Compose
    if command_exists docker-compose || docker compose version >/dev/null 2>&1; then
        print_success "Docker Compose found"
    else
        print_error "Docker Compose not found"
        missing_deps+=("Docker Compose")
    fi
    
    # Check Git
    if command_exists git; then
        GIT_VERSION=$(git --version)
        print_success "Git found: $GIT_VERSION"
    else
        print_error "Git not found"
        missing_deps+=("Git")
    fi
    
    # Check CMake (optional for C++)
    if command_exists cmake; then
        CMAKE_VERSION=$(cmake --version | head -n 1)
        print_success "CMake found: $CMAKE_VERSION"
    else
        print_warning "CMake not found (optional, needed for C++ compilation)"
    fi
    
    # If missing dependencies, exit
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies:"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        exit 1
    fi
    
    print_success "All prerequisites satisfied!"
}

# Create directory structure
create_directories() {
    print_header "Creating Directory Structure"
    
    directories=(
        "backend/app/routes"
        "backend/app/services"
        "backend/app/models"
        "backend/app/utils"
        "backend/algorithms/cpp"
        "backend/algorithms/python"
        "backend/tests/unit"
        "backend/tests/integration"
        "backend/logs"
        "frontend/src/components"
        "frontend/src/pages"
        "frontend/src/hooks"
        "frontend/src/services"
        "frontend/src/store"
        "frontend/src/types"
        "frontend/src/utils"
        "frontend/tests"
        "data/places"
        "data/questions"
        "data/schema"
        "data/scripts"
        "data/examples"
        "docs"
        ".github/workflows"
        "secrets"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_info "Created directory: $dir"
        fi
    done
    
    print_success "Directory structure created!"
}

# Setup environment file
setup_environment() {
    print_header "Setting Up Environment Variables"
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists. Skipping..."
    else
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env from .env.example"
            print_warning "Please edit .env with your actual credentials!"
        else
            print_error ".env.example not found"
            exit 1
        fi
    fi
}

# Setup backend
setup_backend() {
    print_header "Setting Up Backend"
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate || . venv/Scripts/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        print_info "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found"
    fi
    
    cd ..
}

# Setup frontend
setup_frontend() {
    print_header "Setting Up Frontend"
    
    cd frontend
    
    # Install dependencies
    if [ -f "package.json" ]; then
        print_info "Installing Node.js dependencies..."
        npm install
        print_success "Node.js dependencies installed"
    else
        print_warning "package.json not found"
    fi
    
    cd ..
}

# Build C++ modules
build_cpp_modules() {
    print_header "Building C++ Modules"
    
    if command_exists cmake; then
        cd backend/algorithms/cpp
        
        if [ -f "CMakeLists.txt" ]; then
            print_info "Building C++ algorithms..."
            mkdir -p build
            cd build
            cmake ..
            make
            print_success "C++ modules compiled successfully"
            cd ../../../..
        else
            print_warning "CMakeLists.txt not found, skipping C++ build"
            cd ../../..
        fi
    else
        print_warning "CMake not found, skipping C++ build"
    fi
}

# Initialize data files
initialize_data() {
    print_header "Initializing Data Files"
    
    # Create empty data files if they don't exist
    data_files=(
        "data/places/countries.json"
        "data/places/cities.json"
        "data/places/historic_places.json"
        "data/questions/question_bank.json"
    )
    
    for file in "${data_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo "[]" > "$file"
            print_info "Created empty data file: $file"
        fi
    done
    
    print_success "Data files initialized"
}

# Setup Git hooks
setup_git_hooks() {
    print_header "Setting Up Git Hooks"
    
    # Pre-commit hook for validation
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook: Validate data before commit

echo "Running data validation..."
python data/scripts/validate_data.py

if [ $? -ne 0 ]; then
    echo "Data validation failed. Please fix errors before committing."
    exit 1
fi

echo "Data validation passed!"
EOF
    
    chmod +x .git/hooks/pre-commit
    print_success "Git hooks configured"
}

# Test Docker setup
test_docker() {
    print_header "Testing Docker Setup"
    
    print_info "Building Docker images..."
    docker-compose build
    
    print_info "Starting services..."
    docker-compose up -d
    
    # Wait for services to start
    print_info "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Docker services started successfully!"
        
        print_info "Service URLs:"
        echo "  Frontend: http://localhost:5173"
        echo "  Backend:  http://localhost:5000"
        echo "  Redis:    localhost:6379"
        
        # Stop services
        print_info "Stopping services..."
        docker-compose down
    else
        print_error "Failed to start Docker services"
        docker-compose logs
        exit 1
    fi
}

# Create initial test files
create_test_files() {
    print_header "Creating Test Files"
    
    # Backend test
    cat > backend/tests/test_basic.py << 'EOF'
def test_basic():
    """Basic test to ensure pytest is working"""
    assert 1 + 1 == 2
EOF
    
    # Frontend test
    cat > frontend/tests/basic.test.ts << 'EOF'
import { describe, it, expect } from 'vitest';

describe('Basic Test', () => {
  it('should pass', () => {
    expect(1 + 1).toBe(2);
  });
});
EOF
    
    print_success "Test files created"
}

# Print final instructions
print_final_instructions() {
    print_header "Setup Complete! 🎉"
    
    echo "Next steps:"
    echo ""
    echo "1. Edit .env with your Firebase and Redis credentials"
    echo ""
    echo "2. Start development environment:"
    echo "   ${GREEN}docker-compose up${NC}"
    echo ""
    echo "3. Or run services manually:"
    echo "   Terminal 1 (Backend):"
    echo "   ${GREEN}cd backend && source venv/bin/activate && python run.py${NC}"
    echo ""
    echo "   Terminal 2 (Frontend):"
    echo "   ${GREEN}cd frontend && npm run dev${NC}"
    echo ""
    echo "4. Access the application:"
    echo "   Frontend: ${BLUE}http://localhost:5173${NC}"
    echo "   Backend:  ${BLUE}http://localhost:5000${NC}"
    echo ""
    echo "5. Run tests:"
    echo "   ${GREEN}./scripts/test.sh${NC}"
    echo ""
    echo "For more information, see:"
    echo "  - README.md"
    echo "  - docs/ARCHITECTURE.md"
    echo "  - docs/CONTRIBUTING.md"
    echo ""
    print_success "Happy coding! 🚀"
}

# Main execution
main() {
    clear
    print_header "GuessMyPlace - Setup Script"
    
    check_prerequisites
    create_directories
    setup_environment
    initialize_data
    setup_backend
    setup_frontend
    build_cpp_modules
    create_test_files
    
    if command_exists docker; then
        read -p "Do you want to test Docker setup? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            test_docker
        fi
    fi
    
    if command_exists git && [ -d ".git" ]; then
        setup_git_hooks
    fi
    
    print_final_instructions
}

# Run main function
main