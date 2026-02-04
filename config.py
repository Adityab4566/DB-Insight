"""
Configuration management for the Database Monitoring Dashboard.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'db_monitoring')
    DB_USER = os.getenv('DB_USER', 'monitor_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Monitoring Configuration
    REFRESH_INTERVAL = 5  # seconds
    SLOW_QUERY_THRESHOLD = 1.0  # seconds
    CONNECTION_THRESHOLD = 100  # max connections warning
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/monitoring.log'
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration parameters."""
        required_vars = ['DB_PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True