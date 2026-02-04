#!/usr/bin/env python3
"""
Project Health Check Script
Verifies that all components are working correctly.
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist."""
    required_files = [
        'app.py', 'config.py', 'database.py', 'metrics.py',
        'requirements.txt', 'README.md', '.gitignore',
        'templates/dashboard.html', 'static/css/style.css',
        'static/js/dashboard.js'
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All required files present")
    return True

def check_syntax():
    """Check Python syntax."""
    python_files = ['app.py', 'config.py', 'database.py', 'metrics.py', 'run.py']
    
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
        except SyntaxError as e:
            print(f"❌ Syntax error in {file}: {e}")
            return False
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file, 'r', encoding='latin-1') as f:
                    compile(f.read(), file, 'exec')
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
                return False
    
    print("✅ Python syntax check passed")
    return True

if __name__ == "__main__":
    print("🔍 Project Health Check")
    print("=" * 30)
    
    all_good = True
    all_good &= check_files()
    all_good &= check_syntax()
    
    if all_good:
        print("\n🎉 Project is ready for GitHub!")
    else:
        print("\n❌ Please fix the issues above")
        sys.exit(1)