"""
Error handlers for Flask app
"""

from flask import jsonify


def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found'
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'Method not allowed for this endpoint'
            }
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {str(error)}')
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'details': str(error) if app.debug else None
            }
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {str(error)}')
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'details': str(error) if app.debug else None
            }
        }), 500