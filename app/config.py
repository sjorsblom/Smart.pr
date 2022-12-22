from pathlib import Path

database_name="admin"
database_url = f"mongodb://localhost:27017"

class BaseConfig:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': database_name,
        'host': database_url,
        'connect': False
    }

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}