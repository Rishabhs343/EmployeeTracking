# 🐍 PythonAnywhere Deployment Guide - Step by Step

Complete guide to deploy your Employee Performance Tracker on PythonAnywhere with guaranteed data persistence.

## 🎯 Why PythonAnywhere?
- ✅ **100% FREE forever** (no trial periods)
- ✅ **Always-on hosting** (no sleep time)
- ✅ **SQLite database persists forever**
- ✅ **512MB storage** (perfect for employee tracking)
- ✅ **Python-optimized platform**
- ✅ **Professional URL**: yourusername.pythonanywhere.com

---

## 📋 Step 1: Create PythonAnywhere Account

### 1.1 Sign Up
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Click "Pricing & signup" in top menu
3. Choose **"Create a Beginner account"** (FREE option)
4. Fill out registration form:
   - Choose a username (this will be your app URL)
   - Enter email and password
   - **No credit card required!**

### 1.2 Verify Account
- Check your email for verification link
- Click to verify your account
- You're now ready to deploy!

---

## 📁 Step 2: Upload Your Code

### 2.1 Access File Manager
1. Login to PythonAnywhere dashboard
2. Click "Files" tab in top menu
3. You'll see your home directory: `/home/yourusername/`

### 2.2 Upload via Git (Recommended)
1. Click "Consoles" tab
2. Click "Bash" to open terminal
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/Rishabhs343/EmployeeTracking.git

# Navigate to project directory
cd EmployeeTracking

# Check files are there
ls -la
```

### 2.3 Alternative: Manual Upload
If you prefer manual upload:
1. In Files tab, create folder: `EmployeeTracking`
2. Upload all your project files using the file manager
3. Ensure all files are in `/home/yourusername/EmployeeTracking/`

---

## 📦 Step 3: Install Dependencies

### 3.1 Open Bash Console
1. Go to "Consoles" tab
2. Click "Bash" (if not already open)

### 3.2 Install Requirements
```bash
# Navigate to your project (if not already there)
cd EmployeeTracking

# Install dependencies for Python 3.10
pip3.10 install --user -r requirements.txt
```

**Wait for installation to complete** (takes 2-3 minutes)

### 3.3 Verify Installation
```bash
# Test if Flask is installed
python3.10 -c "import flask; print('Flask installed successfully')"

# Test if your app imports correctly
python3.10 -c "from app import app; print('App imports successfully')"
```

---

## 🌐 Step 4: Create Web App

### 4.1 Add New Web App
1. Click "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose your domain: `yourusername.pythonanywhere.com`
4. Click "Next"

### 4.2 Choose Manual Configuration
1. Select **"Manual configuration"**
2. Choose **"Python 3.10"**
3. Click "Next"
4. Your web app is created!

---

## ⚙️ Step 5: Configure Web App

### 5.1 Set Source Code Directory
1. In Web tab, find "Code" section
2. Click on "Source code" field
3. Enter: `/home/yourusername/EmployeeTracking`
4. Click checkmark to save

### 5.2 Configure WSGI File
1. In "Code" section, click on WSGI configuration file link
   (something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
2. Replace ALL content with:

```python
import sys
import os

# Add your project directory to Python path
path = '/home/yourusername/EmployeeTracking'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from run import app as application

if __name__ == "__main__":
    application.run()
```

**Remember to replace `yourusername` with your actual username!**

3. Click "Save" (Ctrl+S)

### 5.3 Set Working Directory
1. Back in Web tab, find "Code" section
2. Set "Working directory" to: `/home/yourusername/EmployeeTracking`
3. Click checkmark to save

---

## 🗄️ Step 6: Initialize Database

### 6.1 Open Python Console
1. Go to "Consoles" tab
2. Click "Python 3.10" console
3. Run these commands:

```python
# Navigate to your project directory
import os
os.chdir('/home/yourusername/EmployeeTracking')

# Import your app and database
from app import app, db

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

### 6.2 Verify Database Creation
```python
# Check if database file exists
import os
print("Database exists:", os.path.exists('instance/performancepro.db'))
```

---

## 🚀 Step 7: Launch Your App

### 7.1 Reload Web App
1. Go back to "Web" tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button
3. Wait for reload to complete (30 seconds)

### 7.2 Access Your App
1. Click on your domain link: `https://yourusername.pythonanywhere.com`
2. Your Employee Performance Tracker should load! 🎉

---

## ✅ Step 8: Test Everything

### 8.1 Test Basic Functionality
1. ✅ Dashboard loads correctly
2. ✅ Navigate to Employees section
3. ✅ Try adding a test employee
4. ✅ Add some performance data
5. ✅ Check analytics dashboard

### 8.2 Test Data Persistence
1. Add a test employee with performance data
2. Note down what you added
3. Restart your app: Web tab → "Reload" button
4. Check if data is still there ✅
5. **Your data persists permanently!**

---

## 🎉 Success! Your App is Live

### What You Now Have:
- ✅ **Live Employee Performance Tracker**
- ✅ **Permanent URL**: `https://yourusername.pythonanywhere.com`
- ✅ **Persistent SQLite database** (data never disappears)
- ✅ **Always-on hosting** (no sleep time)
- ✅ **Free forever** (no time limits)
- ✅ **Professional platform** for your team

### Share with Your Team:
- Send them your PythonAnywhere URL
- They can access it 24/7
- All employee and performance data persists
- Perfect for daily performance tracking!

---

## 🔧 Common Issues & Solutions

### Issue: "No module named 'app'"
**Solution:** Check WSGI file has correct path to your project

### Issue: "Internal Server Error"
**Solution:** 
1. Check Error logs: Web tab → "Error log"
2. Verify all dependencies installed: `pip3.10 install --user -r requirements.txt`

### Issue: Database errors
**Solution:** Re-initialize database in Python console:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### Issue: Static files not loading
**Solution:** PythonAnywhere handles static files automatically for Flask apps

---

## 📈 Usage Monitoring

### Check Your Usage:
1. "Account" tab → shows storage usage
2. "Web" tab → shows web app statistics
3. Monitor to stay within 512MB limit

### Storage Tips:
- Database grows slowly (employee records are small)
- 512MB = sufficient for 50+ employees with full performance history
- Clean old logs occasionally if needed

---

## 🔄 Making Updates

### To Update Your App:
1. Push changes to GitHub
2. In PythonAnywhere Bash console:
```bash
cd EmployeeTracking
git pull origin main
```
3. Reload web app: Web tab → "Reload" button

### For Package Updates:
```bash
pip3.10 install --user -r requirements.txt --upgrade
```

---

## 🎯 Next Steps

1. **Customize your app** - Add your company branding
2. **Train your team** - Show them how to use the performance tracker
3. **Set up regular usage** - Daily performance entry routine
4. **Monitor performance** - Use the analytics dashboard
5. **Consider upgrading** - If you need more storage later ($5/month for 3GB)

**Your Employee Performance Tracker is now live and enterprise-ready!** 🚀