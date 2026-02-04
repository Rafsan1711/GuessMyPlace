"""
Game endpoints - Main game logic routes
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.game_service import GameService
from app.utils.validators import validate_request
import uuid

bp = Blueprint('game', __name__)
game_service = GameService()


@bp.route('/game/start', methods=['POST'])
def start_game():
    """Start a new game session"""
    try:
        data = request.get_json() or {}
        
        # Validate request
        language = data.get('language', 'en')
        category = data.get('category', 'all')
        
        if language not in ['en', 'bn']:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Invalid language. Must be "en" or "bn"'
                }
            }), 400
        
        valid_categories = ['all', 'countries', 'cities', 'historic_places']
        if category not in valid_categories:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': f'Invalid category. Must be one of: {valid_categories}'
                }
            }), 400
        
        # Start game
        result = game_service.start_game(language=language, category=category)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error starting game: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to start game',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/game/answer', methods=['POST'])
def submit_answer():
    """Submit an answer to current question"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Request body is required'
                }
            }), 400
        
        session_id = data.get('session_id')
        answer = data.get('answer')
        
        if not session_id or not answer:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'session_id and answer are required'
                }
            }), 400
        
        valid_answers = ['yes', 'no', 'dont_know', 'probably', 'probably_not']
        if answer not in valid_answers:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_ANSWER',
                    'message': f'Invalid answer. Must be one of: {valid_answers}'
                }
            }), 400
        
        # Process answer
        result = game_service.process_answer(session_id, answer)
        
        if result is None:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'SESSION_NOT_FOUND',
                    'message': 'Game session not found or expired'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error processing answer: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to process answer',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/game/guess', methods=['POST'])
def validate_guess():
    """Validate if the guess was correct"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Request body is required'
                }
            }), 400
        
        session_id = data.get('session_id')
        correct = data.get('correct')
        actual_place_id = data.get('actual_place_id')
        
        if not session_id or correct is None:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'session_id and correct are required'
                }
            }), 400
        
        if not correct and not actual_place_id:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'actual_place_id required when correct=false'
                }
            }), 400
        
        # Validate guess
        result = game_service.validate_guess(session_id, correct, actual_place_id)
        
        if result is None:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'SESSION_NOT_FOUND',
                    'message': 'Game session not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error validating guess: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to validate guess',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/game/state/<session_id>', methods=['GET'])
def get_game_state(session_id):
    """Get current game state"""
    try:
        state = game_service.get_session(session_id)
        
        if state is None:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'SESSION_NOT_FOUND',
                    'message': 'Game session not found or expired'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': state
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting game state: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to get game state',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/game/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback after incorrect guess"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'Request body is required'
                }
            }), 400
        
        session_id = data.get('session_id')
        feedback_type = data.get('feedback_type')
        
        if not session_id or not feedback_type:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_REQUEST',
                    'message': 'session_id and feedback_type are required'
                }
            }), 400
        
        # Process feedback
        result = game_service.process_feedback(session_id, data)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error processing feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to process feedback',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/game/end/<session_id>', methods=['DELETE'])
def end_game(session_id):
    """End a game session"""
    try:
        result = game_service.end_session(session_id)
        
        return jsonify({
            'success': True,
            'data': {
                'session_ended': result,
                'message': 'Game session ended successfully' if result else 'Session not found'
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error ending game: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to end game',
                'details': str(e) if current_app.debug else None
            }
        }), 500