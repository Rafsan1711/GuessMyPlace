"""
Redis client for caching
"""

import redis
import json
from typing import Optional, Dict, Any
from app.models.session import GameSession

# Global Redis client
redis_client = None


def init_redis(app):
    """Initialize Redis client"""
    global redis_client
    
    try:
        redis_url = app.config.get('REDIS_URL')
        
        if redis_url:
            # Use URL (for Upstash or cloud Redis)
            redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
        else:
            # Use individual parameters
            redis_client = redis.Redis(
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0),
                password=app.config.get('REDIS_PASSWORD'),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
        
        # Test connection
        redis_client.ping()
        app.logger.info('Redis initialized successfully')
        
    except Exception as e:
        app.logger.warning(f'Redis not available: {str(e)}')
        redis_client = None


def save_session(session: GameSession) -> bool:
    """Save game session to Redis cache"""
    global redis_client
    
    if redis_client is None:
        return False
    
    try:
        key = f'session:{session.session_id}'
        data = json.dumps(session.to_dict())
        
        # Save with TTL (2 hours)
        redis_client.setex(key, 7200, data)
        return True
        
    except Exception as e:
        print(f'Error saving session to Redis: {e}')
        return False


def get_session(session_id: str) -> Optional[GameSession]:
    """Get game session from Redis cache"""
    global redis_client
    
    if redis_client is None:
        return None
    
    try:
        key = f'session:{session_id}'
        data = redis_client.get(key)
        
        if data is None:
            return None
        
        session_dict = json.loads(data)
        return GameSession.from_dict(session_dict)
        
    except Exception as e:
        print(f'Error getting session from Redis: {e}')
        return None


def delete_session(session_id: str) -> bool:
    """Delete game session from Redis"""
    global redis_client
    
    if redis_client is None:
        return False
    
    try:
        key = f'session:{session_id}'
        redis_client.delete(key)
        return True
        
    except Exception as e:
        print(f'Error deleting session from Redis: {e}')
        return False


def cache_get(key: str) -> Optional[str]:
    """Get value from cache"""
    global redis_client
    
    if redis_client is None:
        return None
    
    try:
        return redis_client.get(key)
    except:
        return None


def cache_set(key: str, value: str, ttl: int = 3600) -> bool:
    """Set value in cache with TTL"""
    global redis_client
    
    if redis_client is None:
        return False
    
    try:
        redis_client.setex(key, ttl, value)
        return True
    except:
        return False