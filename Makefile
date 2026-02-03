.PHONY: help setup test deploy clean docker-up docker-down install format lint

# Default target
help:
	@echo "GuessMyPlace - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Run complete development setup"
	@echo "  make install        - Install dependencies only"
	@echo ""
	@echo "Development:"
	@echo "  make docker-up      - Start all services with Docker"
	@echo "  make docker-down    - Stop all Docker services"
	@echo "  make dev-backend    - Run backend development server"
	@echo "  make dev-frontend   - Run frontend development server"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-backend   - Run backend tests only"
	@echo "  make test-frontend  - Run frontend tests only"
	@echo "  make test-cpp       - Run C++ tests only"
	@echo "  make validate-data  - Validate data files"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format code (Python, TypeScript)"
	@echo "  make lint           - Lint code"
	@echo "  make type-check     - Run type checking"
	@echo ""
	@echo "Data Management:"
	@echo "  make combine-data   - Combine all data files"
	@echo "  make enhance-data   - Enhance data with AI"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-staging - Deploy to staging"
	@echo "  make deploy-prod    - Deploy to production"
	@echo "  make rollback       - Rollback last deployment"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make clean-all      - Remove all generated files"

# Setup
setup:
	@chmod +x scripts/*.sh
	@./scripts/setup.sh

install:
	@echo "Installing backend dependencies..."
	@cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install

# Docker
docker-up:
	@echo "Starting Docker services..."
	@docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:5000"

docker-down:
	@echo "Stopping Docker services..."
	@docker-compose down

docker-logs:
	@docker-compose logs -f

docker-rebuild:
	@echo "Rebuilding Docker images..."
	@docker-compose build --no-cache

# Development
dev-backend:
	@echo "Starting backend development server..."
	@cd backend && source venv/bin/activate && python run.py

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

# Testing
test:
	@chmod +x scripts/test.sh
	@./scripts/test.sh

test-backend:
	@chmod +x scripts/test.sh
	@./scripts/test.sh backend

test-frontend:
	@chmod +x scripts/test.sh
	@./scripts/test.sh frontend

test-cpp:
	@chmod +x scripts/test.sh
	@./scripts/test.sh cpp

validate-data:
	@chmod +x scripts/test.sh
	@./scripts/test.sh data

# Code Quality
format:
	@echo "Formatting Python code..."
	@cd backend && black app/ algorithms/python/
	@echo "Formatting TypeScript code..."
	@cd frontend && npm run format

lint:
	@echo "Linting backend..."
	@cd backend && flake8 app/
	@echo "Linting frontend..."
	@cd frontend && npm run lint

type-check:
	@echo "Type checking backend..."
	@cd backend && mypy app/
	@echo "Type checking frontend..."
	@cd frontend && npm run type-check

# Data Management
combine-data:
	@echo "Combining data files..."
	@python data/scripts/combine_data.py

enhance-data:
	@echo "Enhancing data..."
	@python data/scripts/enhance_data.py

generate-data:
	@echo "Generating new data..."
	@python data/scripts/generate_data.py

# Build
build-backend:
	@echo "Building backend Docker image..."
	@cd backend && docker build -t guessmyplace-backend:latest .

build-frontend:
	@echo "Building frontend..."
	@cd frontend && npm run build

build-cpp:
	@echo "Building C++ modules..."
	@cd backend/algorithms/cpp && mkdir -p build && cd build && cmake .. && make

# Deployment
deploy-staging:
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh staging

deploy-prod:
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh production

deploy-frontend:
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh frontend

deploy-backend:
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh backend

rollback:
	@chmod +x scripts/deploy.sh
	@./scripts/deploy.sh rollback

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf backend/algorithms/cpp/build
	@rm -rf frontend/dist
	@rm -rf frontend/node_modules/.cache
	@echo "Cleanup complete!"

clean-all: clean
	@echo "Removing all dependencies..."
	@rm -rf backend/venv
	@rm -rf frontend/node_modules
	@echo "Full cleanup complete!"

# Git helpers
git-status:
	@git status

git-sync:
	@echo "Syncing with upstream..."
	@git fetch upstream
	@git merge upstream/main

# Database
db-backup:
	@echo "Backing up Firebase database..."
	@python scripts/backup_firebase.py

# Documentation
docs-serve:
	@echo "Serving documentation..."
	@cd docs && python -m http.server 8000

# Stats
stats:
	@echo "Project Statistics:"
	@echo ""
	@echo "Lines of Code:"
	@find backend frontend -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.cpp" | xargs wc -l | tail -1
	@echo ""
	@echo "Data Files:"
	@find data -name "*.json" | wc -l
	@echo ""
	@echo "Tests:"
	@find . -name "*test*.py" -o -name "*test*.ts" | wc -l