#!/usr/bin/env python3
"""
Database Performance Monitoring Dashboard Setup Script
Helps users configure the application for first-time use.
"""

import os
import sys
import getpass
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("🗄️  Database Performance Monitoring Dashboard")
    print("=" * 60)
    print("Welcome! This script will help you set up the application.")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_mysql_connection():
    """Check if MySQL is accessible."""
    try:
        import pymysql
        print("✅ PyMySQL is available")
        return True
    except ImportError:
        print("❌ PyMySQL not found. Please install requirements first:")
        print("   pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file with user input."""
    print("\n🔧 Database Configuration")
    print("Please provide your MySQL database details:")
    
    # Get database configuration
    db_host = input("Database Host [localhost]: ").strip() or "localhost"
    db_port = input("Database Port [3306]: ").strip() or "3306"
    db_name = input("Database Name [db_monitoring]: ").strip() or "db_monitoring"
    db_user = input("Database User [monitor_user]: ").strip() or "monitor_user"
    
    # Get password securely
    while True:
        db_password = getpass.getpass("Database Password: ").strip()
        if db_password:
            break
        print("Password cannot be empty. Please try again.")
    
    # Flask configuration
    print("\n⚙️  Flask Configuration")
    flask_env = input("Flask Environment [development]: ").strip() or "development"
    flask_debug = input("Enable Debug Mode? [y/N]: ").strip().lower()
    flask_debug = "True" if flask_debug in ['y', 'yes'] else "False"
    
    # Create .env content
    env_content = f"""# Database Configuration
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}

# Flask Configuration
FLASK_ENV={flask_env}
FLASK_DEBUG={flask_debug}
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_database_connection():
    """Test database connection with provided credentials."""
    print("\n🔍 Testing database connection...")
    
    try:
        from config import Config
        from database import db_manager
        
        # Test connection
        if db_manager.test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed")
            print("Please check your credentials and ensure MySQL is running")
            return False
            
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ['logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def show_mysql_setup_commands():
    """Show MySQL setup commands."""
    print("\n🗄️  MySQL Setup Commands")
    print("Run these commands in MySQL Workbench or command line:")
    print("-" * 50)
    
    with open('DEMO_COMMANDS.sql', 'r') as f:
        content = f.read()
        # Extract setup commands (first section)
        lines = content.split('\n')
        in_setup = False
        for line in lines:
            if 'SECTION 1: DATABASE SETUP' in line:
                in_setup = True
                continue
            elif 'SECTION 2:' in line:
                break
            elif in_setup and line.strip():
                print(line)
    
    print("-" * 50)

def main():
    """Main setup function."""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies if needed
    if not os.path.exists('.env'):
        print("\n🚀 First-time setup detected")
        
        # Install dependencies
        if not install_dependencies():
            sys.exit(1)
        
        # Show MySQL setup
        show_mysql_setup_commands()
        
        input("\nPress Enter after setting up MySQL database...")
        
        # Create .env file
        if not create_env_file():
            sys.exit(1)
        
        # Create directories
        create_directories()
        
        # Test connection
        if not test_database_connection():
            print("\n⚠️  Database connection failed, but setup is complete.")
            print("Please verify your MySQL setup and credentials.")
        
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Ensure MySQL is running")
        print("2. Run: python run.py")
        print("3. Open: http://localhost:5000")
        
    else:
        print("✅ Application already configured (.env file exists)")
        
        # Just test connection
        if check_mysql_connection():
            test_database_connection()
        
        print("\nTo start the application:")
        print("python run.py")

if __name__ == "__main__":
    main()