import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_database_uri():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # DigitalOcean and Heroku provide postgres:// which SQLAlchemy 2.0+ deprecates
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url
    return f'sqlite:///{BASE_DIR / "instance" / "school.db"}'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-1234567890')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    
    # Upload Settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', str(BASE_DIR / 'app' / 'static' / 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-key-sunny-school-2026')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

