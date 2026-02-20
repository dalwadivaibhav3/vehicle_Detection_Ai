#!/usr/bin/env python3
"""
Setup script for Traffic Vehicle Detection System
This script helps set up the project quickly
"""

import os
import sys
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version}")

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        'static/uploads',
        'static/videos',
        'static/css',
        'static/js',
        'templates',
        'database',
        'models'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def create_gitkeep_files():
    """Create .gitkeep files in empty directories"""
    print_header("Creating .gitkeep Files")
    
    directories = [
        'static/uploads',
        'static/videos'
    ]
    
    for directory in directories:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            pass
        print(f"✅ Created: {gitkeep_path}")

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file from .env.example"""
    print_header("Creating Environment File")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping...")
    else:
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("⚠️  Please update .env file with your configuration!")
        else:
            print("⚠️  .env.example not found. Please create .env manually.")

def print_database_setup():
    """Print database setup instructions"""
    print_header("Database Setup Instructions")
    
    print("""
To set up the database:

1. Install MySQL Server (if not already installed)
   
2. Create the database:
   mysql -u root -p
   CREATE DATABASE traffic_detection;
   EXIT;

3. Update database credentials in .env file:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=traffic_detection

4. Run the database setup script:
   python database/db_setup.py

5. Start the application:
   python app.py
    """)

def print_completion_message():
    """Print completion message"""
    print_header("Setup Complete!")
    
    print("""
✅ Project setup is complete!

Next steps:
1. Configure your database in .env file
2. Run: python database/db_setup.py
3. Run: python app.py
4. Open: http://localhost:5000

For more information, see README.md
    """)

def main():
    """Main setup function"""
    print_header("Traffic Vehicle Detection System - Setup")
    
    try:
        check_python_version()
        create_directories()
        create_gitkeep_files()
        
        # Ask if user wants to install dependencies
        response = input("\nDo you want to install Python dependencies now? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("⏭️  Skipping dependency installation")
        
        create_env_file()
        print_database_setup()
        print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
