"""
Database connection and query management for MySQL monitoring.
Handles all database interactions using read-only access.
"""

import pymysql
import logging
from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and queries for monitoring."""
    
    def __init__(self):
        """Initialize database manager with configuration."""
        self.config = Config()
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                charset='utf8mb4',
                autocommit=True,
                connect_timeout=10,
                read_timeout=30,
                write_timeout=30,
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.error(f"Error closing database connection: {str(e)}")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results."""
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            # Test connection before executing query
            self.connection.ping(reconnect=True)
            
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            logger.error(f"Failed query: {query}")
            # Try to reconnect on connection errors
            if "Lost connection" in str(e) or "gone away" in str(e) or "closed" in str(e):
                logger.info("Attempting to reconnect...")
                self.connection = None
                if self.connect():
                    return self.execute_query(query, params)
            return None
    
    def get_single_value(self, query, params=None):
        """Execute query and return single value."""
        result = self.execute_query(query, params)
        if result and len(result) > 0:
            # Get first value from first row
            first_row = result[0]
            return list(first_row.values())[0]
        return None
    
    def test_connection(self):
        """Test database connectivity."""
        try:
            result = self.get_single_value("SELECT 1 as test")
            return result == 1
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

# Global database manager instance
db_manager = DatabaseManager()