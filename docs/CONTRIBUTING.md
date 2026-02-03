# 🤝 Contributing to GuessMyPlace

First off, thank you for considering contributing to GuessMyPlace! It's people like you that make this project better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

---

## Code of Conduct

This project adheres to a simple code of conduct:
- **Be respectful** and considerate of others
- **Be collaborative** and help each other
- **Be inclusive** and welcoming to all contributors
- **Focus on the code**, not the person

By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**How to submit a good bug report:**
1. Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
2. Provide clear steps to reproduce
3. Include screenshots if applicable
4. Describe expected vs actual behavior
5. Include environment details (OS, browser, etc.)

### ✨ Suggesting Features

Feature suggestions are welcome! Please:
1. Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
2. Explain the problem it solves
3. Describe your proposed solution
4. Consider alternative approaches

### 📊 Adding Data

One of the easiest ways to contribute is by adding new places or questions!

**To add a new place:**
1. Edit the appropriate file in `data/places/`
2. Follow the [data format specification](DATA_FORMAT.md)
3. Run validation: `python data/scripts/validate_data.py`
4. Submit a PR

**To add a new question:**
1. Edit `data/questions/question_bank.json`
2. Ensure the question has good discriminating power
3. Provide both English and Bengali translations
4. Test the question with sample places

### 💻 Code Contributions

We welcome code contributions! Areas include:
- **Frontend**: UI/UX improvements, new features
- **Backend**: API enhancements, performance optimization
- **Algorithms**: Better question selection, ML improvements
- **Testing**: Increase coverage, add test cases
- **Documentation**: Improve docs, add examples
- **DevOps**: CI/CD improvements, Docker optimization

---

## Getting Started

### Prerequisites

Ensure you have:
- **Node.js** 18+ and npm
- **Python** 3.10+
- **Docker** and Docker Compose
- **Git**
- **C++ compiler** (GCC 9+ or Clang 10+)
- **CMake** 3.15+

### Fork & Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/Rafsan1711/GuessMyPlace.git
   cd GuessMyPlace
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Rafsan1711/GuessMyPlace.git
   ```

### Set Up Development Environment

#### Option 1: Docker (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Start all services
docker-compose up
```

Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build C++ modules
cd algorithms/cpp
mkdir build && cd build
cmake ..
make
cd ../../..

# Run backend
python run.py
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Run Tests

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

**C++ Algorithms:**
```bash
cd backend/algorithms/cpp/build
ctest
```

---

## Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bugs
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Test additions
- `perf/` - Performance improvements
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards (below)
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
./scripts/test.sh

# Or manually:
cd backend && pytest
cd frontend && npm test
```

Ensure:
- [ ] All tests pass
- [ ] No linting errors
- [ ] Code coverage hasn't decreased

### 4. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: add new question selection algorithm"
```

See [Commit Guidelines](#commit-guidelines) below for details.

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a PR on GitHub using the [PR template](.github/pull_request_template.md).

---

## Coding Standards

### Python

Follow [PEP 8](https://pep8.org/) with these tools:

```bash
# Format code
black backend/

# Lint
flake8 backend/

# Type check
mypy backend/
```

**Key rules:**
- 4 spaces for indentation
- Max line length: 88 characters (Black default)
- Type hints for function signatures
- Docstrings for all public functions/classes

**Example:**
```python
def calculate_information_gain(
    places: List[Place], 
    question: Question
) -> float:
    """
    Calculate information gain for a question.
    
    Args:
        places: List of possible places
        question: Question to evaluate
        
    Returns:
        Information gain value (0.0 to 1.0)
    """
    # Implementation
    pass
```

### TypeScript/React

Follow [Airbnb Style Guide](https://github.com/airbnb/javascript) with these tools:

```bash
# Format
npm run format

# Lint
npm run lint

# Type check
npm run type-check
```

**Key rules:**
- 2 spaces for indentation
- Use functional components with hooks
- Prefer named exports
- Type everything (no `any`)

**Example:**
```typescript
interface QuestionProps {
  question: Question;
  onAnswer: (answer: Answer) => void;
}

export const QuestionCard: React.FC<QuestionProps> = ({ 
  question, 
  onAnswer 
}) => {
  // Implementation
};
```

### C++

Follow [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html):

```bash
# Format
clang-format -i backend/algorithms/cpp/*.cpp
```

**Key rules:**
- 2 spaces for indentation
- Use modern C++ (C++17+)
- RAII principles
- Const correctness

**Example:**
```cpp
class DecisionTree {
public:
    explicit DecisionTree(const std::vector<Place>& places);
    
    Question selectBestQuestion(
        const std::vector<Answer>& history
    ) const;
    
private:
    std::vector<Place> places_;
    
    double calculateEntropy(
        const std::vector<Place>& subset
    ) const;
};
```

### SQL/JSON

- 2 spaces for indentation
- Alphabetically order keys (when logical)
- Use trailing commas (JSON5 style in data files)

---

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance (dependencies, build, etc.)
- `ci`: CI/CD changes

### Examples

```bash
# Feature
feat(frontend): add dark mode toggle

# Bug fix
fix(backend): resolve session timeout issue

# Documentation
docs(api): update endpoint examples

# Multiple scopes
feat(frontend,backend): implement multiplayer mode

# Breaking change
feat(api)!: change response format

BREAKING CHANGE: API responses now return data in 'result' field
```

### Scope

Common scopes:
- `frontend` - React/TypeScript code
- `backend` - Flask/Python code
- `cpp` - C++ algorithms
- `data` - Data files
- `docs` - Documentation
- `ci` - CI/CD
- `docker` - Docker configuration

---

## Pull Request Process

### Before Submitting

Checklist:
- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] Added tests for new code
- [ ] Updated documentation
- [ ] No merge conflicts with `main`
- [ ] Filled out PR template completely

### PR Title

Use the same format as commit messages:
```
feat(frontend): add statistics dashboard
```

### PR Description

Use the [PR template](.github/pull_request_template.md) and include:
- What changed and why
- Related issues
- Screenshots (for UI changes)
- Testing performed
- Breaking changes (if any)

### Review Process

1. **Automated checks** run via GitHub Actions
   - Tests must pass
   - Linting must pass
   - Build must succeed

2. **Code review** by maintainers
   - At least 1 approval required
   - Address all comments

3. **Final approval** by project lead
   - Check alignment with roadmap
   - Verify documentation

4. **Merge**
   - Squash and merge (default)
   - Delete branch after merge

### After Merge

- Your contribution will be in the next release
- Update your local repo:
  ```bash
  git checkout main
  git pull upstream main
  ```

---

## Project Structure

Understanding the codebase:

```
GuessMyPlace/
├── frontend/              # React app
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API calls
│   │   ├── store/        # State management
│   │   └── types/        # TypeScript types
│   └── tests/            # Frontend tests
│
├── backend/              # Flask API
│   ├── app/
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── models/       # Data models
│   │   └── utils/        # Helpers
│   ├── algorithms/
│   │   ├── cpp/          # C++ engine
│   │   └── python/       # Python algorithms
│   └── tests/            # Backend tests
│
├── data/                 # Static data
│   ├── places/           # Place definitions
│   ├── questions/        # Question bank
│   └── scripts/          # Data tools
│
├── docs/                 # Documentation
└── .github/              # GitHub config
    └── workflows/        # CI/CD
```

### Key Files to Know

- `frontend/src/App.tsx` - Main frontend component
- `backend/app/__init__.py` - Flask app factory
- `backend/algorithms/cpp/decision_tree.cpp` - Core algorithm
- `data/places/combined.json` - All places
- `data/questions/question_bank.json` - All questions

---

## Testing Guidelines

### Unit Tests

**Backend (pytest):**
```python
# backend/tests/unit/test_question_selector.py
def test_select_best_question():
    places = load_test_places()
    question = select_best_question(places, [])
    assert question is not None
    assert question.discriminating_power > 0.5
```

**Frontend (Jest/Vitest):**
```typescript
// frontend/tests/components/QuestionCard.test.tsx
describe('QuestionCard', () => {
  it('renders question text', () => {
    const question = mockQuestion();
    render(<QuestionCard question={question} />);
    expect(screen.getByText(question.text)).toBeInTheDocument();
  });
});
```

### Integration Tests

Test full workflows:
```python
# backend/tests/integration/test_game_flow.py
def test_complete_game_flow(client):
    # Start game
    response = client.post('/api/game/start')
    session_id = response.json['data']['session_id']
    
    # Answer questions
    for _ in range(10):
        response = client.post('/api/game/answer', json={
            'session_id': session_id,
            'answer': 'yes'
        })
        if response.json['data']['type'] == 'guess':
            break
    
    assert response.status_code == 200
```

### Test Coverage

Aim for:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Key flows covered
- **E2E tests**: Critical user journeys

Check coverage:
```bash
# Backend
pytest --cov=backend --cov-report=html

# Frontend
npm run test:coverage
```

---

## Specific Contribution Guides

### Adding a New Place

1. Choose the appropriate file:
   - `data/places/countries.json`
   - `data/places/cities.json`
   - `data/places/historic_places.json`

2. Add entry following [DATA_FORMAT.md](DATA_FORMAT.md):
   ```json
   {
     "id": "statue_of_liberty",
     "name": "Statue of Liberty",
     "type": "historic_place",
     "characteristics": {
       "continent": "north_america",
       "country": "usa",
       "city": "new_york",
       "is_unesco": true,
       "built_year": 1886,
       "is_monument": true,
       "is_statue": true,
       "material": "copper"
     }
   }
   ```

3. Validate:
   ```bash
   python data/scripts/validate_data.py
   ```

4. Test:
   ```bash
   # Start game and try to think of your place
   # Verify it can be guessed correctly
   ```

### Adding a New Question

1. Edit `data/questions/question_bank.json`

2. Add question with translations:
   ```json
   {
     "id": "q_new_001",
     "text": {
       "en": "Is it a statue?",
       "bn": "এটি কি একটি মূর্তি?"
     },
     "characteristic": "is_statue",
     "value": true,
     "discriminating_power": 0.75,
     "category": "type"
   }
   ```

3. Validate:
   ```bash
   python data/scripts/validate_data.py
   ```

### Improving Algorithm

1. Understand current implementation:
   - Read `docs/ARCHITECTURE.md`
   - Study `backend/algorithms/cpp/decision_tree.cpp`

2. Make changes:
   - Keep backward compatibility if possible
   - Add comprehensive tests
   - Benchmark performance

3. Document:
   - Add inline comments
   - Update architecture docs
   - Explain algorithm in PR

### UI/UX Improvements

1. Follow design system:
   - Use Tailwind utility classes
   - Maintain consistent spacing
   - Follow color palette

2. Ensure responsiveness:
   - Test on mobile, tablet, desktop
   - Use responsive Tailwind classes

3. Add animations thoughtfully:
   - Use Framer Motion
   - Keep animations subtle
   - Respect `prefers-reduced-motion`

---

## Need Help?

- 💬 **Discussions**: Ask questions in [GitHub Discussions](https://github.com/Rafsan1711/GuessMyPlace/discussions)
- 🐛 **Issues**: Report bugs or request features
- 📧 **Email**: Contact maintainers (see README)
- 📚 **Docs**: Read [ARCHITECTURE.md](ARCHITECTURE.md) and [API.md](API.md)

---

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub insights

Thank you for contributing! 🎉

---

**Last Updated**: February 2026