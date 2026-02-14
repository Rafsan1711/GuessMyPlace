"""
GuessMyPlace Backend - FastAPI Single File

Production-ready Akinator-style game engine
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
import asyncpg
import redis.asyncio as redis
import os
import json
import math
from uuid import UUID, uuid4
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="GuessMyPlace API",
    description="Akinator-style guessing game for places",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

# Database connection pool
db_pool: Optional[asyncpg.Pool] = None
redis_client: Optional[redis.Redis] = None


# ==================== Pydantic Models ====================

class Place(BaseModel):
    id: Optional[UUID] = None
    name: str
    category: Literal["country", "city", "historic_place"]
    description: Optional[str] = None
    image_url: Optional[str] = None
    characteristics: Dict[str, Any]


class Question(BaseModel):
    id: Optional[UUID] = None
    text: str
    characteristic: str
    expected_value: Any
    category: Literal["country", "city", "historic_place", "all"]
    information_gain_score: float = 0.0


class AnswerType(BaseModel):
    answer: Literal["yes", "no", "probably", "probably_not", "dont_know"]


class StartGameRequest(BaseModel):
    category: Literal["country", "city", "historic_place"]


class AnswerRequest(BaseModel):
    session_id: UUID
    question_id: UUID
    answer: Literal["yes", "no", "probably", "probably_not", "dont_know"]


class GuessResponse(BaseModel):
    session_id: UUID
    guessed_place: Place
    total_questions: int


class FeedbackRequest(BaseModel):
    session_id: UUID
    is_correct: bool
    actual_place_name: Optional[str] = None


class GameSession(BaseModel):
    id: UUID
    category: str
    current_question: Optional[Question] = None
    remaining_count: int
    question_count: int


# ==================== Database Functions ====================

async def get_db():
    """Dependency for database connection"""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not connected")
    return db_pool


async def get_redis():
    """Dependency for Redis connection"""
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not connected")
    return redis_client


async def init_db():
    """Initialize database connection pool"""
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
        logger.info("✅ Database connected")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("✅ Redis connected")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")


async def close_connections():
    """Close all connections"""
    if db_pool:
        await db_pool.close()
    if redis_client:
        await redis_client.close()


# ==================== Game Engine Functions ====================

def calculate_information_gain(places: List[Dict], question: Dict) -> float:
    """
    Calculate information gain for a question.
    Higher score = better question (splits places more evenly)
    """
    if not places:
        return 0.0
    
    characteristic = question["characteristic"]
    expected_value = question["expected_value"]
    
    matches = sum(
        1 for place in places 
        if place["characteristics"].get(characteristic) == expected_value
    )
    
    total = len(places)
    ratio = matches / total if total > 0 else 0
    
    # Entropy-based scoring: best split is 50/50
    # Score ranges from 0 (bad) to 1 (perfect)
    score = 1 - abs(2 * ratio - 1)
    
    return score


def filter_places(places: List[Dict], question: Dict, answer: str) -> List[Dict]:
    """Filter places based on question and answer"""
    characteristic = question["characteristic"]
    expected_value = question["expected_value"]
    
    filtered = []
    for place in places:
        place_value = place["characteristics"].get(characteristic)
        is_match = place_value == expected_value
        
        if answer == "yes":
            if is_match:
                filtered.append(place)
        elif answer == "no":
            if not is_match:
                filtered.append(place)
        elif answer == "probably":
            if is_match or place_value is None:
                filtered.append(place)
        elif answer == "probably_not":
            if not is_match or place_value is None:
                filtered.append(place)
        else:  # dont_know
            filtered.append(place)
    
    return filtered


async def get_places_by_category(conn, category: str) -> List[Dict]:
    """Fetch all places for a category from database"""
    cache_key = f"places:{category}"
    
    # Try cache first
    if redis_client:
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # Fetch from database
    rows = await conn.fetch(
        "SELECT id, name, category, description, image_url, characteristics FROM places WHERE category = $1",
        category
    )
    
    places = [
        {
            "id": str(row["id"]),
            "name": row["name"],
            "category": row["category"],
            "description": row["description"],
            "image_url": row["image_url"],
            "characteristics": row["characteristics"]
        }
        for row in rows
    ]
    
    # Cache for 1 hour
    if redis_client:
        await redis_client.setex(cache_key, 3600, json.dumps(places))
    
    return places


async def get_questions_by_category(conn, category: str) -> List[Dict]:
    """Fetch all questions for a category from database"""
    cache_key = f"questions:{category}"
    
    # Try cache first
    if redis_client:
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # Fetch from database
    rows = await conn.fetch(
        "SELECT id, text, characteristic, expected_value, category FROM questions WHERE category = $1 OR category = 'all'",
        category
    )
    
    questions = [
        {
            "id": str(row["id"]),
            "text": row["text"],
            "characteristic": row["characteristic"],
            "expected_value": row["expected_value"],
            "category": row["category"]
        }
        for row in rows
    ]
    
    # Cache for 1 hour
    if redis_client:
        await redis_client.setex(cache_key, 3600, json.dumps(questions))
    
    return questions


async def select_best_question(places: List[Dict], questions: List[Dict], used_question_ids: List[str]) -> Optional[Dict]:
    """Select the question with highest information gain"""
    if not places or not questions:
        return None
    
    # Filter out used questions
    available_questions = [q for q in questions if q["id"] not in used_question_ids]
    
    if not available_questions:
        return None
    
    # Calculate information gain for each question
    best_question = None
    max_gain = -1
    
    for question in available_questions:
        gain = calculate_information_gain(places, question)
        if gain > max_gain:
            max_gain = gain
            best_question = question
    
    return best_question


async def store_session_state(session_id: str, data: Dict):
    """Store session state in Redis"""
    if redis_client:
        await redis_client.setex(f"session:{session_id}", 3600, json.dumps(data))


async def get_session_state(session_id: str) -> Optional[Dict]:
    """Get session state from Redis"""
    if redis_client:
        cached = await redis_client.get(f"session:{session_id}")
        if cached:
            return json.loads(cached)
    return None


# ==================== API Endpoints ====================

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    await init_db()
    await init_redis()


@app.on_event("shutdown")
async def shutdown_event():
    """Close connections on shutdown"""
    await close_connections()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GuessMyPlace API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    db_status = "healthy" if db_pool else "disconnected"
    redis_status = "healthy" if redis_client else "disconnected"
    
    return {
        "database": db_status,
        "cache": redis_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/game/start")
async def start_game(request: StartGameRequest, db = Depends(get_db)):
    """
    Start a new game session
    Returns: session_id, first question, remaining places count
    """
    try:
        async with db.acquire() as conn:
            # Create game session in database
            session_id = uuid4()
            await conn.execute(
                "INSERT INTO game_sessions (id, category) VALUES ($1, $2)",
                session_id, request.category
            )
            
            # Get all places for this category
            places = await get_places_by_category(conn, request.category)
            
            if not places:
                raise HTTPException(status_code=404, detail=f"No places found for category: {request.category}")
            
            # Get all questions
            questions = await get_questions_by_category(conn, request.category)
            
            if not questions:
                raise HTTPException(status_code=404, detail=f"No questions found for category: {request.category}")
            
            # Select first question
            first_question = await select_best_question(places, questions, [])
            
            # Store session state in Redis
            session_state = {
                "session_id": str(session_id),
                "category": request.category,
                "possible_places": places,
                "used_questions": [],
                "answer_history": []
            }
            await store_session_state(str(session_id), session_state)
            
            return {
                "session_id": session_id,
                "category": request.category,
                "question": first_question,
                "remaining_count": len(places),
                "question_count": 0
            }
            
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/game/answer")
async def submit_answer(request: AnswerRequest, db = Depends(get_db)):
    """
    Submit answer to current question
    Returns: next question or guess
    """
    try:
        # Get session state
        session_state = await get_session_state(str(request.session_id))
        
        if not session_state:
            raise HTTPException(status_code=404, detail="Session not found")
        
        async with db.acquire() as conn:
            # Get question details
            question_row = await conn.fetchrow(
                "SELECT id, text, characteristic, expected_value, category FROM questions WHERE id = $1",
                request.question_id
            )
            
            if not question_row:
                raise HTTPException(status_code=404, detail="Question not found")
            
            question = {
                "id": str(question_row["id"]),
                "text": question_row["text"],
                "characteristic": question_row["characteristic"],
                "expected_value": question_row["expected_value"],
                "category": question_row["category"]
            }
            
            # Filter places based on answer
            possible_places = session_state["possible_places"]
            filtered_places = filter_places(possible_places, question, request.answer)
            
            # Update session state
            session_state["possible_places"] = filtered_places
            session_state["used_questions"].append(str(request.question_id))
            session_state["answer_history"].append({
                "question_id": str(request.question_id),
                "answer": request.answer
            })
            
            # Save answer to database
            await conn.execute(
                """INSERT INTO answer_history (session_id, question_id, answer, remaining_places)
                   VALUES ($1, $2, $3, $4)""",
                request.session_id, request.question_id, request.answer, len(filtered_places)
            )
            
            question_count = len(session_state["answer_history"])
            
            # Decide: ask another question or make a guess
            should_guess = (
                len(filtered_places) <= 2 or
                question_count >= 20 or
                (len(filtered_places) <= 5 and question_count >= 10)
            )
            
            if should_guess and filtered_places:
                # Make a guess
                guessed_place = filtered_places[0]
                
                # Update session
                await conn.execute(
                    "UPDATE game_sessions SET total_questions = $1, guessed_place_id = $2 WHERE id = $3",
                    question_count, UUID(guessed_place["id"]), request.session_id
                )
                
                await store_session_state(str(request.session_id), session_state)
                
                return {
                    "type": "guess",
                    "session_id": request.session_id,
                    "guessed_place": guessed_place,
                    "total_questions": question_count,
                    "remaining_count": len(filtered_places)
                }
            
            elif not filtered_places:
                # No places match - fallback to most likely
                await store_session_state(str(request.session_id), session_state)
                
                return {
                    "type": "no_match",
                    "message": "No places match your answers. Try again!",
                    "session_id": request.session_id
                }
            
            else:
                # Ask next question
                questions = await get_questions_by_category(conn, session_state["category"])
                next_question = await select_best_question(
                    filtered_places,
                    questions,
                    session_state["used_questions"]
                )
                
                if not next_question:
                    # Out of questions, make best guess
                    guessed_place = filtered_places[0]
                    
                    await conn.execute(
                        "UPDATE game_sessions SET total_questions = $1, guessed_place_id = $2 WHERE id = $3",
                        question_count, UUID(guessed_place["id"]), request.session_id
                    )
                    
                    await store_session_state(str(request.session_id), session_state)
                    
                    return {
                        "type": "guess",
                        "session_id": request.session_id,
                        "guessed_place": guessed_place,
                        "total_questions": question_count,
                        "remaining_count": len(filtered_places)
                    }
                
                await store_session_state(str(request.session_id), session_state)
                
                return {
                    "type": "question",
                    "session_id": request.session_id,
                    "question": next_question,
                    "remaining_count": len(filtered_places),
                    "question_count": question_count
                }
                
    except Exception as e:
        logger.error(f"Error submitting answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/game/feedback")
async def submit_feedback(request: FeedbackRequest, db = Depends(get_db)):
    """
    Submit feedback on guess (correct or wrong)
    If wrong, optionally provide actual place name for learning
    """
    try:
        async with db.acquire() as conn:
            # Update session result
            await conn.execute(
                "UPDATE game_sessions SET is_correct = $1, ended_at = NOW() WHERE id = $2",
                request.is_correct, request.session_id
            )
            
            # If wrong, save for learning
            if not request.is_correct and request.actual_place_name:
                session_state = await get_session_state(str(request.session_id))
                
                if session_state:
                    await conn.execute(
                        """INSERT INTO learning_feedback 
                           (session_id, actual_place_name, answer_history)
                           VALUES ($1, $2, $3)""",
                        request.session_id,
                        request.actual_place_name,
                        json.dumps(session_state["answer_history"])
                    )
            
            # Update statistics
            await conn.execute(
                """INSERT INTO statistics (date, total_games, correct_guesses)
                   VALUES (CURRENT_DATE, 1, $1)
                   ON CONFLICT (date) DO UPDATE 
                   SET total_games = statistics.total_games + 1,
                       correct_guesses = statistics.correct_guesses + $1,
                       updated_at = NOW()""",
                1 if request.is_correct else 0
            )
            
            return {
                "status": "success",
                "message": "Thank you for your feedback!"
            }
            
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics(db = Depends(get_db)):
    """Get overall game statistics"""
    try:
        async with db.acquire() as conn:
            stats = await conn.fetchrow("SELECT * FROM game_statistics")
            
            if not stats:
                return {
                    "total_games": 0,
                    "correct_guesses": 0,
                    "accuracy": 0,
                    "avg_questions": 0
                }
            
            accuracy = (stats["correct_guesses"] / stats["total_games"] * 100) if stats["total_games"] > 0 else 0
            
            return {
                "total_games": stats["total_games"],
                "correct_guesses": stats["correct_guesses"],
                "accuracy": round(accuracy, 2),
                "avg_questions": stats["avg_questions"],
                "category_breakdown": {
                    "country": stats["country_games"],
                    "city": stats["city_games"],
                    "historic_place": stats["historic_games"]
                }
            }
            
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
