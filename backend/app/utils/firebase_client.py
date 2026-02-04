"""
Firebase client for database operations
"""

import firebase_admin
from firebase_admin import credentials, db
from typing import Optional, Dict, Any

# Global Firebase app and database reference
firebase_app = None
db_ref = None


def init_firebase(app):
    """Initialize Firebase Admin SDK"""
    global firebase_app, db_ref
    
    try:
        # Check if already initialized
        if firebase_app is not None:
            return
        
        database_url = app.config.get('FIREBASE_DATABASE_URL')
        service_account_path = app.config.get('FIREBASE_SERVICE_ACCOUNT_PATH')
        
        if not database_url:
            app.logger.warning('Firebase Database URL not configured')
            return
        
        # Initialize Firebase
        if service_account_path:
            cred = credentials.Certificate(service_account_path)
        else:
            # Use default credentials (for production)
            cred = credentials.ApplicationDefault()
        
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        
        db_ref = db.reference()
        app.logger.info('Firebase initialized successfully')
        
    except Exception as e:
        app.logger.error(f'Failed to initialize Firebase: {str(e)}')
        firebase_app = None
        db_ref = None


def save_session(session_id: str, data: Dict[str, Any]) -> bool:
    """Save game session to Firebase"""
    global db_ref
    
    if db_ref is None:
        return False
    
    try:
        db_ref.child('sessions').child(session_id).set(data)
        return True
    except Exception as e:
        print(f'Error saving session to Firebase: {e}')
        return False


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get game session from Firebase"""
    global db_ref
    
    if db_ref is None:
        return None
    
    try:
        return db_ref.child('sessions').child(session_id).get()
    except Exception as e:
        print(f'Error getting session from Firebase: {e}')
        return None


def delete_session(session_id: str) -> bool:
    """Delete game session from Firebase"""
    global db_ref
    
    if db_ref is None:
        return False
    
    try:
        db_ref.child('sessions').child(session_id).delete()
        return True
    except Exception as e:
        print(f'Error deleting session from Firebase: {e}')
        return False


def update_stats(stats_data: Dict[str, Any]) -> bool:
    """Update global statistics"""
    global db_ref
    
    if db_ref is None:
        return False
    
    try:
        db_ref.child('statistics').child('global').update(stats_data)
        return True
    except Exception as e:
        print(f'Error updating stats: {e}')
        return False