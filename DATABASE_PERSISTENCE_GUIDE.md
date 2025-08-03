# 🗄️ Database Persistence Guide for Free Hosting

Ensuring your employee performance data persists across server restarts and sleeps.

## ⚠️ The Problem with Ephemeral Storage

Many free hosting platforms use **ephemeral storage**, meaning:
- ❌ Data gets deleted when server restarts
- ❌ SQLite database files disappear
- ❌ All employee and performance data is lost

## ✅ Solutions for Data Persistence

### Option 1: PythonAnywhere (Best for SQLite)
**Data Persistence: ✅ GUARANTEED**
- Persistent file storage even on free tier
- SQLite database files survive restarts
- 512MB storage limit (sufficient for most use cases)

### Option 2: External Database Services (Recommended)
**Data Persistence: ✅ GUARANTEED**

#### A) Railway Database (Free)
- PostgreSQL database with 1GB storage
- Separate from web app hosting
- Survives all restarts

#### B) PlanetScale (Free MySQL)
- 10GB storage, 1 billion reads/month
- Automatic backups
- High performance

#### C) Supabase (Free PostgreSQL)
- 500MB storage, 2GB bandwidth
- Real-time features
- Built-in authentication

#### D) ElephantSQL (Free PostgreSQL)
- 20MB storage (good for small teams)
- Reliable and fast

### Option 3: Railway + External DB
- Host app on Railway (fast, reliable)
- Use external database for persistence
- Best of both worlds

## 🔧 Implementation Guide

### For External PostgreSQL Database:

✅ **Already implemented in your app!**

1. **Requirements updated** - Added `psycopg2-binary==2.9.7`
2. **App.py updated** - Added PostgreSQL support with SQLite fallback

## 🚀 Step-by-Step Setup

### Option A: Railway Database + Railway Hosting

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create Database First**
   - New Project → "Provision PostgreSQL"
   - Note the connection details

3. **Deploy Your App**
   - New Service → "GitHub Repo"
   - Add environment variable: `DATABASE_URL` (copy from PostgreSQL service)

4. **Benefits:**
   - ✅ 1GB PostgreSQL database (free)
   - ✅ Fast hosting for your app
   - ✅ Data persists forever
   - ✅ Automatic backups

### Option B: PlanetScale Database + Any Hosting

1. **Create PlanetScale Account**
   - Go to [planetscale.com](https://planetscale.com)
   - Create free database

2. **Get Connection String**
   - Format: `mysql://username:password@host:port/database?sslcert=path`

3. **Update requirements.txt for MySQL:**
   ```
   PyMySQL==1.1.0
   ```

4. **Set Environment Variables:**
   - `MYSQL_HOST`
   - `MYSQL_USERNAME` 
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`

### Option C: Supabase Database + Any Hosting

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Create new project

2. **Get PostgreSQL Connection String**
   - Go to Settings → Database
   - Copy connection string

3. **Set Environment Variable:**
   - `DATABASE_URL=postgresql://user:pass@host:port/db`

### Option D: PythonAnywhere (SQLite with Persistence)

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Free tier includes persistent storage

2. **Upload Your Code**
   ```bash
   git clone your-repo-url
   cd your-project
   pip3.10 install --user -r requirements.txt
   ```

3. **Configure Web App**
   - Web tab → Add new web app
   - Manual configuration → Python 3.10
   - Set source code directory

4. **Database automatically persists** - No additional setup needed!

## 🎯 Recommended Approach

**For Maximum Reliability:**

```
🏆 Best Setup: Railway Database + Railway Hosting
├── ✅ 1GB PostgreSQL database (persistent)
├── ✅ Fast app hosting 
├── ✅ Automatic deployments from GitHub
├── ✅ Custom domains
└── ✅ No sleep time

🥈 Alternative: PythonAnywhere 
├── ✅ SQLite with persistent storage
├── ✅ Python-focused platform
├── ✅ Always-on (no sleep)
└── ⚠️ 512MB storage limit
```

## 🧪 Test Data Persistence

After deployment, test persistence:

1. **Add test employee and performance data**
2. **Wait for server to sleep/restart** (or force restart)
3. **Check if data is still there**

## 🔧 Environment Variables Setup

Set these on your hosting platform:

```bash
# For PostgreSQL (Railway/Supabase)
DATABASE_URL=postgresql://user:pass@host:port/database

# For MySQL (PlanetScale)  
MYSQL_HOST=your-host
MYSQL_USERNAME=your-username
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=your-database

# App Security
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

## 📊 Storage Comparison

| Platform | Storage | Persistence | Restart Behavior |
|----------|---------|-------------|------------------|
| Railway (PostgreSQL) | 1GB | ✅ PERMANENT | Data survives all restarts |
| PlanetScale | 10GB | ✅ PERMANENT | Data survives all restarts |
| Supabase | 500MB | ✅ PERMANENT | Data survives all restarts |
| PythonAnywhere | 512MB | ✅ PERMANENT | Data survives all restarts |
| Render (SQLite) | Ephemeral | ❌ TEMPORARY | Data lost on restart |

## 🚨 Important Notes

1. **Always backup your data** - Even with persistent storage
2. **Test thoroughly** - Deploy and restart to verify persistence  
3. **Monitor storage usage** - Most free tiers have limits
4. **Consider upgrading** - When your team grows beyond free limits

Your Employee Performance Tracker will now maintain all employee records, performance data, and bonus calculations across any server restarts! 🎉