# 🏗️ GuessMyPlace - System Architecture

## Overview

GuessMyPlace is built on a modern, scalable architecture that separates concerns and enables independent development of components. The system follows a client-server model with intelligent algorithms powered by C++ for performance-critical operations.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         React + TypeScript Frontend (Vite)             │ │
│  │  - Component-based UI                                   │ │
│  │  - State management (Zustand/Context)                   │ │
│  │  - Tailwind CSS styling                                 │ │
│  │  - Framer Motion animations                             │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│                    HTTPS REST API                            │
│                            ↓                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        SERVER TIER                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Flask Application Server                   │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │   Routes     │  │  Services    │  │   Models     │ │ │
│  │  │ (REST API)   │→ │ (Business    │→ │  (Data       │ │ │
│  │  │              │  │  Logic)      │  │   Structures)│ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │ │
│  │                           │                             │ │
│  │                           ↓                             │ │
│  │  ┌────────────────────────────────────────────────────┐│ │
│  │  │         C++ Performance Engine (via pybind11)      ││ │
│  │  │  - Decision Tree Algorithm                          ││ │
│  │  │  - Information Gain Calculator                      ││ │
│  │  │  - Probability Scoring Engine                       ││ │
│  │  └────────────────────────────────────────────────────┘│ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│                            ↓                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         DATA TIER                            │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │  Firebase RTDB   │        │   Redis Cache    │          │
│  │  - Sessions      │        │   (Upstash)      │          │
│  │  - User stats    │        │   - Questions    │          │
│  │  - Game history  │        │   - Probabilities│          │
│  └──────────────────┘        └──────────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Static JSON Data (Git)                   │  │
│  │  - places/countries.json                              │  │
│  │  - places/cities.json                                 │  │
│  │  - places/historic_places.json                        │  │
│  │  - questions/question_bank.json                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (React + TypeScript)

#### Directory Structure
```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Game/
│   │   │   ├── QuestionCard.tsx
│   │   │   ├── AnswerButtons.tsx
│   │   │   ├── ProgressIndicator.tsx
│   │   │   └── GuessReveal.tsx
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Container.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Loading.tsx
│   │       └── ErrorBoundary.tsx
│   ├── pages/            # Page components
│   │   ├── Home.tsx
│   │   ├── Game.tsx
│   │   ├── Stats.tsx
│   │   └── About.tsx
│   ├── hooks/            # Custom React hooks
│   │   ├── useGame.ts
│   │   ├── useApi.ts
│   │   └── useLocalStorage.ts
│   ├── services/         # API communication
│   │   ├── api.ts
│   │   └── gameApi.ts
│   ├── store/            # State management
│   │   └── gameStore.ts
│   ├── types/            # TypeScript definitions
│   │   ├── game.types.ts
│   │   └── api.types.ts
│   ├── utils/            # Helper functions
│   │   └── helpers.ts
│   ├── App.tsx
│   └── main.tsx
```

#### Key Technologies
- **React 18**: Component rendering with hooks
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Zustand**: Lightweight state management
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Animations

#### State Management
```typescript
interface GameState {
  sessionId: string | null;
  currentQuestion: Question | null;
  answeredQuestions: Answer[];
  possiblePlaces: Place[];
  gamePhase: 'idle' | 'playing' | 'guessing' | 'finished';
  guess: Place | null;
  statistics: GameStats;
}
```

### 2. Backend (Flask + Python + C++)

#### Directory Structure
```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── game.py          # Game endpoints
│   │   ├── stats.py         # Statistics endpoints
│   │   └── health.py        # Health check
│   ├── services/
│   │   ├── __init__.py
│   │   ├── game_service.py  # Core game logic
│   │   ├── session_service.py
│   │   ├── question_service.py
│   │   └── learning_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── place.py
│   │   ├── question.py
│   │   ├── session.py
│   │   └── answer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── firebase_client.py
│   │   ├── redis_client.py
│   │   └── validators.py
│   └── config.py
├── algorithms/
│   ├── cpp/
│   │   ├── decision_tree.cpp
│   │   ├── decision_tree.h
│   │   ├── information_gain.cpp
│   │   ├── information_gain.h
│   │   ├── probability_engine.cpp
│   │   ├── probability_engine.h
│   │   ├── bindings.cpp     # pybind11 bindings
│   │   └── CMakeLists.txt
│   └── python/
│       ├── __init__.py
│       ├── question_selector.py
│       ├── answer_analyzer.py
│       └── learning_engine.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt
├── run.py                   # Entry point
└── Dockerfile
```

#### Key Technologies
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin support
- **pybind11**: Python-C++ bindings
- **firebase-admin**: Firebase SDK
- **redis-py**: Redis client
- **pytest**: Testing framework

#### API Endpoints

##### Game Management
```
POST   /api/game/start
POST   /api/game/answer
GET    /api/game/state/:sessionId
POST   /api/game/guess
POST   /api/game/feedback
DELETE /api/game/end
```

##### Statistics
```
GET    /api/stats/global
GET    /api/stats/places
GET    /api/stats/questions
```

##### Health
```
GET    /health
GET    /api/health/detailed
```

### 3. C++ Performance Engine

#### Core Algorithms

##### Decision Tree
```cpp
class DecisionTree {
public:
    Question selectBestQuestion(
        const std::vector<Place>& possiblePlaces,
        const std::vector<Answer>& history
    );
    
    double calculateInformationGain(
        const Question& question,
        const std::vector<Place>& places
    );
    
private:
    double calculateEntropy(const std::vector<Place>& places);
    std::vector<Place> filterByAnswer(
        const std::vector<Place>& places,
        const Question& q,
        Answer answer
    );
};
```

##### Probability Engine
```cpp
class ProbabilityEngine {
public:
    std::map<Place, double> calculateProbabilities(
        const std::vector<Place>& places,
        const std::vector<Answer>& answers
    );
    
    Place getMostLikely(const std::map<Place, double>& probs);
    
private:
    double bayesianUpdate(
        double prior,
        double likelihood,
        double evidence
    );
};
```

### 4. Data Layer

#### Firebase Realtime Database Schema
```json
{
  "sessions": {
    "session_id": {
      "created_at": "timestamp",
      "user_id": "string (optional)",
      "current_question_index": 0,
      "answer_history": [],
      "possible_places": [],
      "status": "playing | finished",
      "guess": null,
      "correct": null
    }
  },
  "statistics": {
    "global": {
      "total_games": 0,
      "correct_guesses": 0,
      "average_questions": 0
    },
    "places": {
      "place_id": {
        "games_played": 0,
        "times_guessed": 0,
        "average_questions": 0
      }
    }
  }
}
```

#### Redis Cache Structure
```
Key Pattern                     TTL    Description
-------------------------------------------------
session:{id}                    2h     Session data
question:cache:{hash}           1h     Computed questions
probability:{session_id}        2h     Place probabilities
stats:global                    5m     Global statistics
places:by:characteristic:{key}  24h    Place filtering
```

#### Static JSON Data Format

##### Place Format
```json
{
  "id": "eiffel_tower",
  "name": "Eiffel Tower",
  "type": "historic_place",
  "characteristics": {
    "continent": "europe",
    "country": "france",
    "city": "paris",
    "is_unesco": true,
    "built_year": 1889,
    "is_monument": true,
    "is_building": true,
    "has_observation_deck": true,
    "material": "iron",
    "architectural_style": "art_nouveau"
  }
}
```

##### Question Format
```json
{
  "id": "q001",
  "text": {
    "en": "Is it in Europe?",
    "bn": "এটি কি ইউরোপে?"
  },
  "characteristic": "continent",
  "value": "europe",
  "discriminating_power": 0.85,
  "category": "location"
}
```

## Data Flow

### Game Start Flow
```
1. User clicks "Start Game"
   ↓
2. Frontend sends POST /api/game/start
   ↓
3. Backend creates session in Firebase
   ↓
4. C++ engine loads all places
   ↓
5. Question selector picks first question
   ↓
6. Response sent with session_id + first question
   ↓
7. Frontend displays question
```

### Answer Flow
```
1. User clicks answer (Yes/No/etc.)
   ↓
2. Frontend sends POST /api/game/answer
   ↓
3. Backend retrieves session from Firebase/Redis
   ↓
4. C++ engine filters possible places
   ↓
5. Probability engine calculates likelihoods
   ↓
6. If confidence > 85%: Make guess
   If confidence < 85%: Ask another question
   ↓
7. Update session in Firebase + cache in Redis
   ↓
8. Return next question or guess
   ↓
9. Frontend displays result
```

### Learning Flow (Wrong Guess)
```
1. User says "No, that's wrong"
   ↓
2. Frontend sends POST /api/game/feedback
   ↓
3. Backend analyzes answer history
   ↓
4. Identifies discriminating questions
   ↓
5. Suggests new questions to add
   ↓
6. Updates place characteristics if needed
   ↓
7. Logs for future ML training
```

## Performance Considerations

### C++ Usage
- **Decision tree operations**: 10-100x faster than Python
- **Probability calculations**: Vectorized operations
- **Memory efficiency**: Direct memory access

### Caching Strategy
- **L1 Cache (Redis)**: Frequently accessed data (sessions, computed results)
- **L2 Cache (Firebase)**: Persistent session data
- **L3 Cache (Static JSON)**: Place and question data

### Optimization Techniques
1. **Lazy Loading**: Load places on-demand
2. **Precomputation**: Cache information gain for common questions
3. **Indexing**: Create indices on place characteristics
4. **Batch Processing**: Process multiple answers together

## Scalability

### Horizontal Scaling
- **Frontend**: Static site, infinitely scalable via CDN
- **Backend**: Stateless API, can run multiple instances
- **Database**: Firebase auto-scales
- **Cache**: Redis can be clustered

### Load Handling
- **Rate Limiting**: 60 requests/minute per IP
- **Request Queuing**: Background job processing
- **Connection Pooling**: Reuse database connections

## Security

### API Security
- **CORS**: Whitelist allowed origins
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs
- **HTTPS Only**: Enforce secure connections

### Data Security
- **Environment Variables**: Secrets never in code
- **Firebase Rules**: Restrict database access
- **Session Tokens**: Validate on each request

## Monitoring & Logging

### Application Logs
```python
# Structured logging
logger.info("Game started", extra={
    "session_id": session_id,
    "timestamp": datetime.now(),
    "user_agent": request.headers.get("User-Agent")
})
```

### Metrics to Track
- API response times
- Question selection time
- Guess accuracy
- Cache hit rates
- Error rates
- User engagement

## Deployment Architecture

### Vercel (Frontend)
```
GitHub Push → Vercel Build → CDN Distribution
```

### Hugging Face Space (Backend)
```
GitHub Push → HF Sync → Docker Build → Container Deploy
```

### CI/CD Pipeline
```
Code Push
    ↓
Run Tests (GitHub Actions)
    ↓
Build Docker Image
    ↓
Push to Registry
    ↓
Deploy to HF Space
    ↓
Health Check
    ↓
Update DNS (if needed)
```

## Development Workflow

### Local Development
```bash
# Terminal 1: Backend
cd backend
docker-compose up

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Testing
```bash
# Unit tests
pytest backend/tests/unit/
npm test

# Integration tests
pytest backend/tests/integration/

# E2E tests
npm run test:e2e
```

## Future Architecture Enhancements

1. **GraphQL API**: Replace REST for flexible queries
2. **WebSocket**: Real-time multiplayer support
3. **Microservices**: Split services (game, stats, ML)
4. **Event Sourcing**: Track all game events
5. **CQRS**: Separate read/write models
6. **Message Queue**: Async processing (RabbitMQ/Redis)
7. **ML Pipeline**: Automated model training
8. **A/B Testing**: Experiment with algorithms

## Conclusion

GuessMyPlace's architecture is designed for:
- **Performance**: C++ for critical operations
- **Scalability**: Stateless design, horizontal scaling
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Modular components, easy to enhance
- **Developer Experience**: Simple local setup, clear interfaces

For specific implementation details, see:
- [API Documentation](API.md)
- [Data Format](DATA_FORMAT.md)
- [Contributing Guide](CONTRIBUTING.md)