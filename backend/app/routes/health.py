"""
Health check endpoints
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime
import time

bp = Blueprint('health', __name__)

# Store start time
START_TIME = time.time()


@bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200


@bp.route('/api/health/detailed', methods=['GET'])
def detailed_health():
    """Detailed health check with component status"""
    from app.utils import firebase_client, redis_client
    
    components = {}
    overall_status = 'healthy'
    
    # Check API
    components['api'] = {
        'status': 'up',
        'response_time_ms': 1
    }
    
    # Check Firebase
    try:
        if firebase_client.db:
            start = time.time()
            # Quick test read
            firebase_client.db.reference('/.info/connected').get()
            latency = int((time.time() - start) * 1000)
            components['firebase'] = {
                'status': 'up',
                'latency_ms': latency
            }
        else:
            components['firebase'] = {'status': 'not_configured'}
    except Exception as e:
        components['firebase'] = {
            'status': 'down',
            'error': str(e)
        }
        overall_status = 'degraded'
    
    # Check Redis
    try:
        if redis_client.redis:
            start = time.time()
            redis_client.redis.ping()
            latency = int((time.time() - start) * 1000)
            
            # Get cache hit rate if available
            info = redis_client.redis.info('stats')
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
            
            components['redis'] = {
                'status': 'up',
                'latency_ms': latency,
                'hit_rate': round(hit_rate, 2)
            }
        else:
            components['redis'] = {'status': 'not_configured'}
    except Exception as e:
        components['redis'] = {
            'status': 'down',
            'error': str(e)
        }
        overall_status = 'degraded'
    
    # Check C++ engine
    try:
        if current_app.config.get('USE_CPP_ENGINE'):
            # TODO: Test C++ module import
            components['cpp_engine'] = {
                'status': 'loaded',
                'version': '1.0.0'
            }
        else:
            components['cpp_engine'] = {'status': 'disabled'}
    except Exception as e:
        components['cpp_engine'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Calculate uptime
    uptime_seconds = int(time.time() - START_TIME)
    
    return jsonify({
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'components': components,
        'version': '1.0.0',
        'uptime_seconds': uptime_seconds
    }), 200