"""
Simple run script for the Database Performance Monitoring Dashboard.
Provides a clean way to start the application with error handling.
"""

import os
import sys
from app import app, logger, Config

def check_environment():
    """Check if environment is properly configured."""
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found")
        print("Please run 'python setup.py' first to configure the application")
        return False
    
    try:
        Config.validate_config()
        return True
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file")
        return False

def main():
    """Main function to run the application."""
    print("🗄️  Starting Database Performance Monitoring Dashboard...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        # Print startup info
        print(f"🌐 Server will start at: http://localhost:5000")
        print(f"🔧 Environment: {Config.FLASK_ENV}")
        print(f"📊 Database: {Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}")
        print("Press Ctrl+C to stop\n")
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.FLASK_DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()