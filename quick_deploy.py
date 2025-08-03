#!/usr/bin/env python3
"""
Quick Deployment Script for PerformancePro
Tests deployment readiness and sets up for data persistence
"""

import os
import sys
import subprocess
import shutil

def check_git_status():
    """Check git repository status"""
    print("📂 Checking git repository...")
    
    if not os.path.exists('.git'):
        print("❌ No git repository found. Initializing...")
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
    
    # Check for remote
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    if not result.stdout.strip():
        print("⚠️  No git remote found. You'll need to:")
        print("   git remote add origin https://github.com/yourusername/your-repo.git")
        return False
    else:
        print("✅ Git remote configured")
        return True

def prepare_for_deployment():
    """Prepare application for deployment with data persistence"""
    print("\n🚀 Preparing for deployment with data persistence...")
    
    # Check required files
    required_files = {
        'Procfile': 'web: gunicorn run:app --host 0.0.0.0 --port $PORT',
        'railway.json': '{"build": {"builder": "NIXPACKS"}, "deploy": {"startCommand": "gunicorn run:app --host 0.0.0.0 --port $PORT"}}',
        'runtime.txt': 'python-3.11.0'
    }
    
    for file, content in required_files.items():
        if not os.path.exists(file):
            print(f"📝 Creating {file}...")
            with open(file, 'w') as f:
                f.write(content)
            print(f"✅ {file} created")
        else:
            print(f"✅ {file} exists")
    
    print("✅ Deployment files ready")

def show_deployment_options():
    """Show deployment options with data persistence"""
    print("\n🎯 RECOMMENDED DEPLOYMENT OPTIONS (with Data Persistence)")
    print("=" * 60)
    
    print("\n🏆 OPTION 1: Railway (Database + Hosting)")
    print("   Data Persistence: ✅ GUARANTEED")
    print("   Steps:")
    print("   1. Go to railway.app")
    print("   2. Create new project → Provision PostgreSQL")
    print("   3. Deploy from GitHub repo")
    print("   4. Connect DATABASE_URL environment variable")
    print("   Benefits: 1GB database, fast hosting, no sleep time")
    
    print("\n🥈 OPTION 2: PythonAnywhere")
    print("   Data Persistence: ✅ GUARANTEED")
    print("   Steps:")
    print("   1. Go to pythonanywhere.com")
    print("   2. Upload code via git")
    print("   3. Create web app (manual config)")
    print("   4. SQLite database automatically persists")
    print("   Benefits: Python-focused, always-on, 512MB storage")
    
    print("\n🥉 OPTION 3: Render + External Database")
    print("   Data Persistence: ✅ GUARANTEED")
    print("   Steps:")
    print("   1. Create database on Supabase/PlanetScale")
    print("   2. Deploy app on Render")
    print("   3. Set DATABASE_URL environment variable")
    print("   Benefits: Fast hosting + reliable database")
    
    print("\n❌ AVOID: Render with SQLite (data gets lost)")

def test_database_config():
    """Test database configuration"""
    print("\n🗄️ Testing database configuration...")
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        from app import app, db
        
        with app.app_context():
            # Test database URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"📍 Database URI: {db_uri.split('@')[0]}@***" if '@' in db_uri else db_uri)
            
            if 'postgresql://' in db_uri or 'mysql://' in db_uri:
                print("✅ External database configured (data will persist)")
            elif 'sqlite://' in db_uri:
                print("⚠️  SQLite configured (only persists on PythonAnywhere)")
            
            # Test database creation
            db.create_all()
            print("✅ Database tables created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def commit_changes():
    """Commit all changes to git"""
    print("\n📝 Committing changes...")
    
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            subprocess.run(['git', 'commit', '-m', 'Prepare for deployment with data persistence'], check=True)
            print("✅ Changes committed")
        else:
            print("✅ No changes to commit")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Git commit failed")
        return False

def main():
    """Main deployment preparation function"""
    print("🚀 PerformancePro Quick Deployment Setup")
    print("=" * 50)
    print("🎯 Focus: Data Persistence Across Server Restarts")
    print("=" * 50)
    
    steps = [
        ("Check Git Repository", check_git_status),
        ("Prepare Deployment Files", prepare_for_deployment), 
        ("Test Database Configuration", test_database_config),
        ("Commit Changes", commit_changes)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"❌ {step_name} failed")
    
    print(f"\n📊 Setup Complete: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("\n🎉 Ready for deployment!")
        show_deployment_options()
        
        print("\n📚 Additional Resources:")
        print("   📖 DATABASE_PERSISTENCE_GUIDE.md - Detailed persistence guide")
        print("   📖 DEPLOYMENT_GUIDE.md - Complete deployment instructions")
        
        print("\n🚀 Next Steps:")
        print("   1. Push to GitHub: git push origin main")
        print("   2. Choose a hosting platform from options above")
        print("   3. Follow platform-specific setup")
        print("   4. Test data persistence after deployment")
        
    else:
        print("\n⚠️  Please fix the issues above before deploying")

if __name__ == "__main__":
    main()