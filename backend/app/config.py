"""
Configuration classes for different environments
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""
    
    # App settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Firebase
    FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
    FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    
    # Cache settings
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))
    SESSION_TTL = int(os.getenv('SESSION_TTL', 7200))
    
    # API settings
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    API_VERSION = os.getenv('API_VERSION', 'v1')
    MAX_QUESTIONS_PER_GAME = int(os.getenv('MAX_QUESTIONS_PER_GAME', 30))
    DEFAULT_CONFIDENCE_THRESHOLD = float(os.getenv('DEFAULT_CONFIDENCE_THRESHOLD', 0.85))
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    RATE_LIMIT_PER_HOUR = int(os.getenv('RATE_LIMIT_PER_HOUR', 1000))
    
    # Algorithm settings
    USE_CPP_ENGINE = os.getenv('USE_CPP_ENGINE', 'True').lower() == 'true'
    CPP_LIB_PATH = os.getenv('CPP_LIB_PATH', './algorithms/cpp/build/libdecision_engine.so')
    QUESTION_STRATEGY = os.getenv('QUESTION_STRATEGY', 'information_gain')
    MIN_INFORMATION_GAIN = float(os.getenv('MIN_INFORMATION_GAIN', 0.1))
    
    # Data paths
    DATA_PATH = os.getenv('DATA_PATH', './data')
    PLACES_FILE = os.getenv('PLACES_FILE', './data/places/combined.json')
    QUESTIONS_FILE = os.getenv('QUESTIONS_FILE', './data/questions/question_bank.json')
    AUTO_RELOAD_DATA = os.getenv('AUTO_RELOAD_DATA', 'True').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory Redis for testing
    REDIS_URL = 'redis://localhost:6379/15'


# Configuration dictionary - THIS IS CRITICAL
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Make config dict available at module level
__all__ = ['config', 'Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']
