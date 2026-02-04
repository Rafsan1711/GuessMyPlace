#!/usr/bin/env python3
"""
GuessMyPlace Backend - Main Entry Point
"""

import os
import sys
from app import create_app
from app.config import config

# Get configuration name from environment
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app = create_app(config_name)

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║        🌍  GuessMyPlace Backend API  🌍       ║
    ║                                               ║
    ║  Environment: {config_name:20s}          ║
    ║  Host: {host:25s}               ║
    ║  Port: {port:25d}               ║
    ║  Debug: {str(debug):24s}               ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    
    API Documentation: http://{host}:{port}/api/docs
    Health Check: http://{host}:{port}/health
    
    Press CTRL+C to quit
    """)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )