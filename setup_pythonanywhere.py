#!/usr/bin/env python3
"""
PythonAnywhere Setup Script
Run this script in PythonAnywhere console to set up your Employee Performance Tracker
"""

import os
import sys

def setup_database():
    """Initialize the database with default data"""
    print("🗄️ Setting up database...")
    
    try:
        # Import Flask app
        from app import app, db
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created")
            
            # Check if database file exists
            from app import Department, Employee
            if Department.query.count() == 0:
                print("📝 Creating default departments...")
                # Will be created automatically by init_enterprise_db
            
            if Employee.query.count() == 0:
                print("👤 Creating sample employee...")
                # Will be created automatically by init_enterprise_db
            
            print("✅ Database setup complete!")
            return True
            
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("📦 Testing imports...")
    
    required_modules = [
        'flask', 'flask_sqlalchemy', 'openpyxl', 
        'datetime', 'calendar', 'json'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n🔧 Install missing modules with:")
        print(f"pip3.10 install --user {' '.join(missing_modules)}")
        return False
    
    print("✅ All imports successful!")
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        'app.py', 'run.py', 'requirements.txt',
        'templates/dashboard.html', 'templates/base.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {missing_files}")
        return False
    
    print("✅ All files present!")
    return True

def create_instance_directory():
    """Create instance directory for database"""
    print("📂 Creating instance directory...")
    
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"✅ Created {instance_dir} directory")
    else:
        print(f"✅ {instance_dir} directory exists")
    
    return True

def main():
    """Main setup function"""
    print("🐍 PythonAnywhere Setup for Employee Performance Tracker")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"📍 Current directory: {current_dir}")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Please navigate to your project directory first:")
        print("   cd EmployeeTracking")
        return False
    
    # Run setup steps
    steps = [
        ("Check File Structure", check_file_structure),
        ("Test Imports", test_imports),
        ("Create Instance Directory", create_instance_directory),
        ("Setup Database", setup_database)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"❌ {step_name} failed")
    
    print(f"\n📊 Setup Results: {success_count}/{len(steps)} steps completed")
    
    if success_count == len(steps):
        print("\n🎉 Setup Complete!")
        print("\n📝 Next Steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Create a new web app (Manual configuration, Python 3.10)")
        print("3. Set source code directory to your project path")
        print("4. Configure WSGI file (see PYTHONANYWHERE_DEPLOYMENT.md)")
        print("5. Reload your web app")
        print("\n🌐 Your app will be available at: https://yourusername.pythonanywhere.com")
    else:
        print("\n⚠️ Please fix the issues above before proceeding")
    
    return success_count == len(steps)

if __name__ == "__main__":
    main()