"""
Database Performance Monitoring Dashboard
Main Flask application for real-time MySQL performance monitoring.
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from config import Config
from database import db_manager
from metrics import metrics_collector

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Validate configuration on startup
try:
    Config.validate_config()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration validation failed: {str(e)}")
    print(f"ERROR: {str(e)}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

@app.route('/')
def dashboard():
    """Render the main dashboard page."""
    try:
        logger.info("Dashboard page requested")
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Error rendering dashboard: {str(e)}")
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/api/metrics')
def get_metrics():
    """API endpoint to get all performance metrics as JSON."""
    try:
        logger.debug("Metrics API endpoint called")
        
        # Collect all metrics
        metrics = metrics_collector.collect_all_metrics()
        
        # Add API metadata
        metrics['api_version'] = '1.0'
        metrics['server_time'] = datetime.now().isoformat()
        
        logger.debug(f"Metrics collected: {metrics['health_status']}")
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"Error collecting metrics: {str(e)}")
        error_response = {
            'error': True,
            'message': str(e),
            'timestamp': datetime.now().isoformat(),
            'health_status': 'ERROR'
        }
        return jsonify(error_response), 500

@app.route('/api/health')
def health_check():
    """API endpoint for basic health check."""
    try:
        logger.debug("Health check endpoint called")
        
        # Test database connectivity
        is_healthy = db_manager.test_connection()
        
        health_data = {
            'status': 'UP' if is_healthy else 'DOWN',
            'database_connected': is_healthy,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        status_code = 200 if is_healthy else 503
        logger.info(f"Health check result: {health_data['status']}")
        
        return jsonify(health_data), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        error_response = {
            'status': 'ERROR',
            'database_connected': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(error_response), 500

@app.route('/api/config')
def get_config():
    """API endpoint to get non-sensitive configuration information."""
    try:
        config_info = {
            'database_host': Config.DB_HOST,
            'database_port': Config.DB_PORT,
            'database_name': Config.DB_NAME,
            'database_user': Config.DB_USER,
            'refresh_interval': Config.REFRESH_INTERVAL,
            'slow_query_threshold': Config.SLOW_QUERY_THRESHOLD,
            'connection_threshold': Config.CONNECTION_THRESHOLD,
            'flask_env': Config.FLASK_ENV
        }
        
        logger.debug("Configuration info requested")
        return jsonify(config_info)
        
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500
    }), 500

def initialize_app():
    """Initialize application components."""
    try:
        logger.info("Initializing application...")
        
        # Test database connection
        if db_manager.test_connection():
            logger.info("Database connection test successful")
        else:
            logger.warning("Database connection test failed - monitoring will show errors")
        
        logger.info("Application initialized successfully")
        
    except Exception as e:
        logger.error(f"Application initialization failed: {str(e)}")

# Initialize app components
with app.app_context():
    initialize_app()

@app.teardown_appcontext
def close_db_connection(error):
    """Close database connection when app context tears down."""
    if error:
        logger.error(f"App context error: {str(error)}")
    
    try:
        db_manager.disconnect()
    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}")

def create_app():
    """Application factory function."""
    return app

if __name__ == '__main__':
    try:
        logger.info("Starting Database Performance Monitoring Dashboard...")
        logger.info(f"Configuration: {Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}")
        logger.info(f"Environment: {Config.FLASK_ENV}")
        
        # Print startup information
        print("=" * 60)
        print("🗄️  Database Performance Monitoring Dashboard")
        print("=" * 60)
        print(f"📊 Dashboard URL: http://localhost:5000")
        print(f"🔗 API Metrics: http://localhost:5000/api/metrics")
        print(f"❤️  Health Check: http://localhost:5000/api/health")
        print(f"🔧 Database: {Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}")
        print(f"👤 User: {Config.DB_USER}")
        print(f"🔄 Refresh: {Config.REFRESH_INTERVAL}s")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.FLASK_DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        print("\n👋 Dashboard stopped. Goodbye!")
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        print(f"❌ Error starting dashboard: {str(e)}")
        print("Please check your configuration and database connection.")
        
    finally:
        # Cleanup
        try:
            db_manager.disconnect()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")