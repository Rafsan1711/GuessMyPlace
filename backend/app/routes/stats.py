"""
Statistics endpoints
"""

from flask import Blueprint, jsonify, current_app
from app.services.stats_service import StatsService

bp = Blueprint('stats', __name__)
stats_service = StatsService()


@bp.route('/stats/global', methods=['GET'])
def get_global_stats():
    """Get overall game statistics"""
    try:
        stats = stats_service.get_global_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting global stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to get statistics',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/stats/places/<place_id>', methods=['GET'])
def get_place_stats(place_id):
    """Get statistics for a specific place"""
    try:
        stats = stats_service.get_place_stats(place_id)
        
        if stats is None:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': f'Place not found: {place_id}'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting place stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to get place statistics',
                'details': str(e) if current_app.debug else None
            }
        }), 500


@bp.route('/stats/questions', methods=['GET'])
def get_question_stats():
    """Get statistics about question effectiveness"""
    try:
        stats = stats_service.get_question_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting question stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Failed to get question statistics',
                'details': str(e) if current_app.debug else None
            }
        }), 500