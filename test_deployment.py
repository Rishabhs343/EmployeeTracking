#!/usr/bin/env python3
"""
PerformancePro Deployment Test Script
Tests if the application is ready for deployment
"""

import os
import sys
import subprocess
import importlib.util

def test_python_version():
    """Test if Python version is compatible"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible (need 3.8+)")
        return False

def test_dependencies():
    """Test if all dependencies are available"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'flask', 'flask_sqlalchemy', 'gunicorn', 
        'openpyxl', 'werkzeug', 'sqlalchemy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_app_import():
    """Test if the app can be imported"""
    print("\n🚀 Testing app import...")
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try importing the app
        from app import app, db
        print("✅ App imports successfully")
        
        # Test if database can be created
        with app.app_context():
            db.create_all()
            print("✅ Database creation successful")
        
        return True
    except Exception as e:
        print(f"❌ App import failed: {str(e)}")
        return False

def test_files_exist():
    """Test if required deployment files exist"""
    print("\n📄 Testing deployment files...")
    
    required_files = [
        'requirements.txt', 'Procfile', 'railway.json', 
        'render.yaml', 'app.py', 'run.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} is missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_git_repository():
    """Test if git repository is set up"""
    print("\n📂 Testing git repository...")
    
    if os.path.exists('.git'):
        print("✅ Git repository exists")
        
        # Check if there are uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️  There are uncommitted changes")
            print("   Run: git add . && git commit -m 'Ready for deployment'")
        else:
            print("✅ No uncommitted changes")
        
        return True
    else:
        print("❌ Git repository not found")
        print("   Run: git init && git add . && git commit -m 'Initial commit'")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 PerformancePro Deployment Readiness Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_files_exist,
        test_app_import,
        test_git_repository
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Your app is ready for deployment!")
        print("\n🚀 Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Choose hosting platform (see DEPLOYMENT_GUIDE.md)")
        print("3. Deploy and enjoy! 🎉")
    else:
        print("⚠️  Please fix the issues above before deploying")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)