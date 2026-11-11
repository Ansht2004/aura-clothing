import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'aura-apparel-super-secure-jwt-secret-key-2026')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'aura-apparel-jwt-token-key-2026-mca')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # Database URI with PostgreSQL and SQLite support
    _raw_db_url = os.getenv('DATABASE_URL')
    if _raw_db_url and _raw_db_url.startswith('postgres://'):
        _raw_db_url = _raw_db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = _raw_db_url or f"sqlite:///{os.path.join(BASE_DIR, 'aura_clothing.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    } if 'mysql' in os.getenv('DATABASE_URL', '') else {}

    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Store settings (Indian Rupees ₹)
    TAX_RATE = 0.12  # 12% GST
    DEFAULT_SHIPPING_FEE = 149.00  # ₹149 standard shipping
    FREE_SHIPPING_THRESHOLD = 2499.00  # Free shipping on orders over ₹2,499


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'test_aura_clothing.db')}"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
