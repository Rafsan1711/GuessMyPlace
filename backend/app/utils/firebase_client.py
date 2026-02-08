"""
Firebase client for database operations
"""

import os
import json
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
            app.logger.info('Firebase already initialized')
            return
        
        database_url = os.getenv('FIREBASE_DATABASE_URL')
        
        if not database_url:
            app.logger.warning('FIREBASE_DATABASE_URL not configured - Firebase disabled')
            return
        
        # Try to get service account from JSON string (HF Space method)
        service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
        
        if service_account_json:
            # Parse JSON string and create credentials
            try:
                service_account_dict = json.loads(service_account_json)
                cred = credentials.Certificate(service_account_dict)
                app.logger.info('Using Firebase service account from JSON env var')
            except json.JSONDecodeError as e:
                app.logger.error(f'Failed to parse FIREBASE_SERVICE_ACCOUNT_JSON: {e}')
                return
        
        # Try to build service account from individual env vars
        elif all([
            os.getenv('FIREBASE_TYPE'),
            os.getenv('FIREBASE_PROJECT_ID'),
            os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            os.getenv('FIREBASE_PRIVATE_KEY'),
            os.getenv('FIREBASE_CLIENT_EMAIL'),
            os.getenv('FIREBASE_CLIENT_ID'),
        ]):
            # Build service account dict from individual variables
            service_account_dict = {
                "type": os.getenv('FIREBASE_TYPE'),
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
            }
            cred = credentials.Certificate(service_account_dict)
            app.logger.info('Using Firebase service account from individual env vars')
        
        # Try to use service account file path
        else:
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                app.logger.info(f'Using Firebase service account from file: {service_account_path}')
            else:
                # Try application default credentials (for GCP environments)
                try:
                    cred = credentials.ApplicationDefault()
                    app.logger.info('Using Firebase application default credentials')
                except Exception as e:
                    app.logger.error(f'No valid Firebase credentials found: {e}')
                    app.logger.warning('Firebase will be disabled')
                    return
        
        # Initialize Firebase app
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        
        # Get database reference
        db_ref = db.reference()
        
        app.logger.info(f'✓ Firebase initialized successfully with database: {database_url}')
        
    except Exception as e:
        app.logger.error(f'Failed to initialize Firebase: {str(e)}')
        app.logger.exception(e)
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


def get_stats() -> Optional[Dict[str, Any]]:
    """Get global statistics"""
    global db_ref
    
    if db_ref is None:
        return None
    
    try:
        return db_ref.child('statistics').child('global').get()
    except Exception as e:
        print(f'Error getting stats: {e}')
        return None


def is_initialized() -> bool:
    """Check if Firebase is initialized"""
    return firebase_app is not None and db_ref is not None
