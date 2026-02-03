#!/bin/bash

# GuessMyPlace - Deployment Script
# Deploys frontend to Vercel and syncs backend to Hugging Face Space

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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "Must run from project root directory"
        exit 1
    fi
}

# Verify environment
verify_environment() {
    print_header "Verifying Environment"
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        print_error ".env file not found"
        exit 1
    fi
    
    # Source .env
    source .env
    
    # Verify critical env vars
    if [ -z "$FIREBASE_DATABASE_URL" ]; then
        print_error "FIREBASE_DATABASE_URL not set in .env"
        exit 1
    fi
    
    print_success "Environment verified"
}

# Run tests before deployment
run_tests() {
    print_header "Running Tests"
    
    print_info "Running test suite..."
    ./scripts/test.sh
    
    if [ $? -ne 0 ]; then
        print_error "Tests failed. Aborting deployment."
        exit 1
    fi
    
    print_success "All tests passed"
}

# Build frontend
build_frontend() {
    print_header "Building Frontend"
    
    cd frontend
    
    print_info "Installing dependencies..."
    npm ci
    
    print_info "Building production bundle..."
    npm run build
    
    if [ ! -d "dist" ]; then
        print_error "Build failed - dist directory not found"
        cd ..
        exit 1
    fi
    
    print_success "Frontend built successfully"
    cd ..
}

# Deploy to Vercel
deploy_frontend() {
    print_header "Deploying Frontend to Vercel"
    
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
    
    cd frontend
    
    print_info "Deploying to Vercel..."
    
    # Check if it's a production deployment
    if [ "${1}" == "production" ]; then
        vercel --prod --yes
    else
        vercel --yes
    fi
    
    print_success "Frontend deployed to Vercel"
    cd ..
}

# Build backend Docker image
build_backend() {
    print_header "Building Backend Docker Image"
    
    cd backend
    
    print_info "Building Docker image..."
    docker build -t guessmyplace-backend:latest .
    
    print_success "Backend Docker image built"
    cd ..
}

# Test backend locally
test_backend_docker() {
    print_header "Testing Backend Docker Image"
    
    print_info "Starting backend container..."
    docker run -d --name guessmyplace-test \
        -p 5001:5000 \
        -e FLASK_ENV=production \
        guessmyplace-backend:latest
    
    # Wait for container to start
    sleep 5
    
    # Health check
    print_info "Performing health check..."
    if curl -f http://localhost:5001/health; then
        print_success "Backend health check passed"
    else
        print_error "Backend health check failed"
        docker logs guessmyplace-test
        docker stop guessmyplace-test
        docker rm guessmyplace-test
        exit 1
    fi
    
    # Cleanup
    docker stop guessmyplace-test
    docker rm guessmyplace-test
    
    print_success "Backend Docker image tested successfully"
}

# Sync to Hugging Face Space
sync_to_huggingface() {
    print_header "Syncing to Hugging Face Space"
    
    # Check if git remote for HF is configured
    if ! git remote | grep -q "huggingface"; then
        print_warning "Hugging Face remote not configured"
        print_info "Configure with: git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE"
        
        read -p "Do you want to configure it now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter HF Space URL: " hf_url
            git remote add huggingface "$hf_url"
            print_success "Hugging Face remote added"
        else
            print_error "Hugging Face remote required for deployment"
            exit 1
        fi
    fi
    
    # Commit backend changes
    print_info "Committing backend changes..."
    git add backend/
    git commit -m "Deploy: Update backend" || print_warning "No backend changes to commit"
    
    # Push to HF Space
    print_info "Pushing to Hugging Face Space..."
    git push huggingface main:main
    
    print_success "Backend synced to Hugging Face Space"
    print_info "Space will rebuild automatically"
    print_info "Monitor at: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE"
}

# Update data files
update_data() {
    print_header "Updating Data Files"
    
    print_info "Validating data..."
    python data/scripts/validate_data.py
    
    print_info "Combining data files..."
    python data/scripts/combine_data.py
    
    print_success "Data files updated"
}

# Create deployment tag
create_tag() {
    print_header "Creating Deployment Tag"
    
    # Get current version from package.json
    VERSION=$(node -p "require('./frontend/package.json').version")
    TAG="v${VERSION}-$(date +%Y%m%d-%H%M%S)"
    
    print_info "Creating tag: $TAG"
    git tag -a "$TAG" -m "Deployment $TAG"
    git push origin "$TAG"
    
    print_success "Tag created: $TAG"
}

# Deployment summary
print_summary() {
    print_header "Deployment Summary"
    
    echo "Deployment completed successfully! 🚀"
    echo ""
    echo "Frontend:"
    echo "  Status: Deployed to Vercel"
    echo "  URL: Check Vercel dashboard"
    echo ""
    echo "Backend:"
    echo "  Status: Synced to Hugging Face Space"
    echo "  URL: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE"
    echo ""
    echo "Next steps:"
    echo "  1. Monitor Hugging Face Space build logs"
    echo "  2. Test production endpoints"
    echo "  3. Update DNS if needed"
    echo ""
}

# Rollback deployment
rollback() {
    print_header "Rolling Back Deployment"
    
    print_info "Rolling back to previous deployment..."
    
    # Rollback Vercel
    cd frontend
    if command -v vercel &> /dev/null; then
        vercel rollback
    fi
    cd ..
    
    # Rollback HF Space (revert git commit)
    git revert HEAD --no-edit
    git push huggingface main:main
    
    print_success "Rollback completed"
}

# Main deployment flow
deploy() {
    local ENVIRONMENT="${1:-staging}"
    
    print_header "GuessMyPlace Deployment - ${ENVIRONMENT}"
    
    check_directory
    verify_environment
    
    # Ask for confirmation
    print_warning "You are about to deploy to ${ENVIRONMENT}"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    # Run deployment steps
    run_tests
    update_data
    build_frontend
    build_backend
    test_backend_docker
    
    # Deploy based on environment
    if [ "$ENVIRONMENT" == "production" ]; then
        deploy_frontend production
        sync_to_huggingface
        create_tag
    else
        deploy_frontend staging
        print_info "Skipping HF sync for staging"
    fi
    
    print_summary
}

# Parse command line arguments
case "${1:-}" in
    production|prod)
        deploy "production"
        ;;
    staging)
        deploy "staging"
        ;;
    frontend)
        build_frontend
        deploy_frontend "${2:-staging}"
        ;;
    backend)
        build_backend
        test_backend_docker
        sync_to_huggingface
        ;;
    data)
        update_data
        ;;
    rollback)
        rollback
        ;;
    test)
        run_tests
        ;;
    *)
        echo "GuessMyPlace Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  production    Deploy to production (Vercel + HF Space)"
        echo "  staging       Deploy to staging (Vercel only)"
        echo "  frontend      Deploy only frontend"
        echo "  backend       Deploy only backend"
        echo "  data          Update and validate data files"
        echo "  test          Run tests without deploying"
        echo "  rollback      Rollback last deployment"
        echo ""
        echo "Examples:"
        echo "  $0 production    # Full production deployment"
        echo "  $0 staging       # Deploy to staging"
        echo "  $0 frontend      # Deploy only frontend"
        echo "  $0 backend       # Deploy only backend"
        echo "  $0 rollback      # Rollback deployment"
        exit 1
        ;;
esac