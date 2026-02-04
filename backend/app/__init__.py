"""
GuessMyPlace Backend Application Factory
"""

from flask import Flask
from flask_cors import CORS
from app.config import config


def create_app(config_name='development'):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    from app.routes import health, game, stats
    
    app.register_blueprint(health.bp)
    app.register_blueprint(game.bp, url_prefix='/api')
    app.register_blueprint(stats.bp, url_prefix='/api')
    
    # Error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Initialize services
    with app.app_context():
        from app.utils import firebase_client, redis_client
        
        # Initialize Firebase
        if app.config.get('FIREBASE_DATABASE_URL'):
            firebase_client.init_firebase(app)
        
        # Initialize Redis
        if app.config.get('REDIS_URL'):
            redis_client.init_redis(app)
    
    # Logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/guessmyplace.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('GuessMyPlace startup')
    
    return app