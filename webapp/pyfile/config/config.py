import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'anykey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///BTS.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MESSAGE_DB_URI = os.environ.get('DATABASE_URL', 'sqlite:///message_database.db')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    UPLOAD_FOLDER = '/uploads/'  # Correction ici
    SQLALCHEMY_BINDS = {
        'messages': MESSAGE_DB_URI
    }