# 🔌 GuessMyPlace API Documentation

## Base URL
```
Development: http://localhost:5000/api
Production:  https://your-space.hf.space/api
```

## Authentication
Currently, the API does not require authentication. Session management is handled via `session_id` returned on game start.

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  }
}
```

## Error Codes
- `INVALID_REQUEST`: Malformed request
- `SESSION_NOT_FOUND`: Invalid or expired session
- `INVALID_ANSWER`: Answer format is incorrect
- `GAME_ALREADY_FINISHED`: Attempt to modify finished game
- `INTERNAL_ERROR`: Server error
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## Game Endpoints

### Start New Game

Start a new guessing game session.

**Endpoint**: `POST /api/game/start`

**Request Body**:
```json
{
  "language": "en",  // Optional: "en" or "bn", default "en"
  "category": "all"  // Optional: "countries", "cities", "historic_places", "all"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "session_id": "uuid-v4-string",
    "question": {
      "id": "q001",
      "text": "Is it in Europe?",
      "question_number": 1,
      "total_questions_asked": 1
    },
    "possible_places_count": 500,
    "answer_options": [
      { "value": "yes", "label": "Yes" },
      { "value": "no", "label": "No" },
      { "value": "dont_know", "label": "Don't Know" },
      { "value": "probably", "label": "Probably" },
      { "value": "probably_not", "label": "Probably Not" }
    ]
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "category": "all"}'
```

---

### Submit Answer

Submit an answer to the current question.

**Endpoint**: `POST /api/game/answer`

**Request Body**:
```json
{
  "session_id": "uuid-v4-string",
  "answer": "yes"  // "yes", "no", "dont_know", "probably", "probably_not"
}
```

**Response (Next Question)**: `200 OK`
```json
{
  "success": true,
  "data": {
    "type": "question",
    "question": {
      "id": "q042",
      "text": "Is it a UNESCO World Heritage Site?",
      "question_number": 5,
      "total_questions_asked": 5
    },
    "possible_places_count": 23,
    "confidence": 0.45,
    "progress_percentage": 17
  }
}
```

**Response (Guess)**: `200 OK`
```json
{
  "success": true,
  "data": {
    "type": "guess",
    "guess": {
      "id": "eiffel_tower",
      "name": "Eiffel Tower",
      "type": "historic_place",
      "details": {
        "country": "France",
        "city": "Paris",
        "built_year": 1889,
        "description": "Iconic iron lattice tower..."
      },
      "image_url": "https://example.com/images/eiffel.jpg"
    },
    "confidence": 0.92,
    "total_questions_asked": 8,
    "alternative_guesses": [
      {
        "id": "arc_de_triomphe",
        "name": "Arc de Triomphe",
        "confidence": 0.05
      }
    ]
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/game/answer \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "answer": "yes"
  }'
```

---

### Validate Guess

User confirms if the guess was correct or incorrect.

**Endpoint**: `POST /api/game/guess`

**Request Body**:
```json
{
  "session_id": "uuid-v4-string",
  "correct": true,  // true if guess was correct, false otherwise
  "actual_place_id": "louvre_museum"  // Required if correct=false
}
```

**Response (Correct)**: `200 OK`
```json
{
  "success": true,
  "data": {
    "result": "correct",
    "message": "Great! I guessed correctly! 🎉",
    "statistics": {
      "questions_asked": 8,
      "time_taken_seconds": 45,
      "accuracy_rate": 0.92
    },
    "share_text": "I played GuessMyPlace and it guessed Eiffel Tower in 8 questions!",
    "play_again": true
  }
}
```

**Response (Incorrect)**: `200 OK`
```json
{
  "success": true,
  "data": {
    "result": "incorrect",
    "message": "I was wrong! It was Louvre Museum.",
    "feedback_requested": true,
    "suggested_questions": [
      {
        "text": "Is it an art museum?",
        "would_help": true
      }
    ],
    "learning_opportunity": {
      "place_added": false,
      "characteristics_updated": true
    }
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/game/guess \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "correct": false,
    "actual_place_id": "louvre_museum"
  }'
```

---

### Submit Feedback

Submit feedback after an incorrect guess to help improve the algorithm.

**Endpoint**: `POST /api/game/feedback`

**Request Body**:
```json
{
  "session_id": "uuid-v4-string",
  "feedback_type": "missing_question",  // "missing_question", "wrong_characteristic", "other"
  "suggested_question": {
    "text": "Is it an art museum?",
    "characteristic": "type",
    "value": "art_museum"
  },
  "comment": "Optional user comment"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "feedback_recorded": true,
    "message": "Thank you for helping us improve!",
    "contribution_id": "contrib-uuid"
  }
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/game/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc-123",
    "feedback_type": "missing_question",
    "suggested_question": {
      "text": "Is it an art museum?",
      "characteristic": "type",
      "value": "art_museum"
    }
  }'
```

---

### Get Game State

Retrieve current state of a game session.

**Endpoint**: `GET /api/game/state/:sessionId`

**Parameters**:
- `sessionId` (path): Session ID

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "session_id": "abc-123",
    "status": "playing",  // "playing", "guessing", "finished"
    "current_question": {
      "id": "q010",
      "text": "Is it in Asia?"
    },
    "answers_given": [
      { "question_id": "q001", "answer": "yes" },
      { "question_id": "q005", "answer": "no" }
    ],
    "possible_places_count": 45,
    "questions_asked": 3,
    "created_at": "2026-02-02T10:30:00Z",
    "last_updated": "2026-02-02T10:32:15Z"
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/game/state/abc-123
```

---

### End Game

End a game session (cleanup).

**Endpoint**: `DELETE /api/game/end/:sessionId`

**Parameters**:
- `sessionId` (path): Session ID

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "session_ended": true,
    "message": "Game session ended successfully"
  }
}
```

**Example**:
```bash
curl -X DELETE http://localhost:5000/api/game/end/abc-123
```

---

## Statistics Endpoints

### Get Global Statistics

Get overall game statistics.

**Endpoint**: `GET /api/stats/global`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "total_games_played": 15420,
    "correct_guesses": 12336,
    "accuracy_rate": 0.80,
    "average_questions_per_game": 9.3,
    "most_popular_places": [
      { "id": "eiffel_tower", "name": "Eiffel Tower", "games": 342 },
      { "id": "great_wall", "name": "Great Wall of China", "games": 298 }
    ],
    "last_updated": "2026-02-02T10:35:00Z"
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/stats/global
```

---

### Get Place Statistics

Get statistics for a specific place.

**Endpoint**: `GET /api/stats/places/:placeId`

**Parameters**:
- `placeId` (path): Place ID

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "place_id": "eiffel_tower",
    "name": "Eiffel Tower",
    "games_featured": 342,
    "times_guessed": 289,
    "guess_accuracy": 0.84,
    "average_questions": 8.2,
    "frequently_confused_with": [
      { "id": "arc_de_triomphe", "name": "Arc de Triomphe", "count": 23 }
    ]
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/stats/places/eiffel_tower
```

---

### Get Question Statistics

Get statistics about question effectiveness.

**Endpoint**: `GET /api/stats/questions`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "total_questions": 234,
    "average_discriminating_power": 0.72,
    "most_effective_questions": [
      {
        "id": "q001",
        "text": "Is it in Europe?",
        "discriminating_power": 0.95,
        "times_asked": 14230
      }
    ],
    "least_effective_questions": [
      {
        "id": "q187",
        "text": "Was it built in the 20th century?",
        "discriminating_power": 0.23,
        "times_asked": 1230
      }
    ]
  }
}
```

**Example**:
```bash
curl http://localhost:5000/api/stats/questions
```

---

## Health Check Endpoints

### Basic Health Check

Simple health check endpoint.

**Endpoint**: `GET /health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-02-02T10:30:00Z"
}
```

**Example**:
```bash
curl http://localhost:5000/health
```

---

### Detailed Health Check

Detailed health check with component status.

**Endpoint**: `GET /api/health/detailed`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-02-02T10:30:00Z",
  "components": {
    "api": {
      "status": "up",
      "response_time_ms": 3
    },
    "firebase": {
      "status": "up",
      "latency_ms": 45
    },
    "redis": {
      "status": "up",
      "latency_ms": 2,
      "hit_rate": 0.87
    },
    "cpp_engine": {
      "status": "loaded",
      "version": "1.0.0"
    }
  },
  "version": "1.0.0",
  "uptime_seconds": 3456789
}
```

**Example**:
```bash
curl http://localhost:5000/api/health/detailed
```

---

## Rate Limiting

All endpoints are rate-limited:
- **Default**: 60 requests per minute per IP
- **Burst**: 100 requests per minute
- **Headers returned**:
  - `X-RateLimit-Limit`: Max requests per window
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

**Example Headers**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1706875200
```

**Rate Limit Exceeded Response**: `429 Too Many Requests`
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after_seconds": 30
  }
}
```

---

## CORS

CORS is enabled for the following origins:
- `http://localhost:5173` (development)
- `https://yourdomain.com` (production)

Allowed methods: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

---

## Webhooks (Future)

Webhooks for real-time updates (planned feature):

### Game Events
```json
{
  "event": "game.finished",
  "timestamp": "2026-02-02T10:30:00Z",
  "data": {
    "session_id": "abc-123",
    "result": "correct",
    "questions_asked": 8
  }
}
```

---

## SDKs & Client Libraries (Future)

Planned client libraries:
- JavaScript/TypeScript
- Python
- Go
- Ruby

---

## API Versioning

Current version: `v1`

Version is included in URL: `/api/v1/...`

Breaking changes will result in new version: `/api/v2/...`

---

## Best Practices

1. **Store session_id**: Keep track of the session ID throughout the game
2. **Handle errors**: Always check `success` field in responses
3. **Respect rate limits**: Implement exponential backoff
4. **Use timeouts**: Set reasonable request timeouts (5-10 seconds)
5. **Cache when possible**: Cache static data like place details
6. **Validate input**: Always validate user input before sending

---

## Example: Complete Game Flow

```javascript
// 1. Start game
const startResponse = await fetch('/api/game/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ language: 'en', category: 'all' })
});
const { session_id, question } = (await startResponse.json()).data;

// 2. Answer questions
while (true) {
  const answer = getUserAnswer(); // "yes", "no", etc.
  
  const answerResponse = await fetch('/api/game/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, answer })
  });
  
  const result = (await answerResponse.json()).data;
  
  if (result.type === 'guess') {
    // Show guess to user
    showGuess(result.guess);
    break;
  } else {
    // Show next question
    showQuestion(result.question);
  }
}

// 3. Validate guess
const correct = userConfirmsGuess();
const validateResponse = await fetch('/api/game/guess', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    session_id, 
    correct,
    actual_place_id: correct ? null : getActualPlaceId()
  })
});

// 4. Show results
const finalResult = (await validateResponse.json()).data;
showResults(finalResult);
```

---

## Questions?

For issues or questions about the API:
- Open an issue on GitHub
- Check the [Architecture Docs](ARCHITECTURE.md)
- Join our discussions

Last Updated: February 2026