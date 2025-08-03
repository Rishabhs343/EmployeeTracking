#!/bin/bash

# PerformancePro Deployment Script
# This script helps prepare your application for deployment

echo "🚀 PerformancePro Deployment Preparation"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Initializing..."
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check for Procfile
if [ ! -f "Procfile" ]; then
    echo "❌ Procfile not found!"
    exit 1
fi

echo "✅ All deployment files ready"

# Commit changes
read -p "📝 Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Prepare for deployment"
fi

git commit -m "$commit_msg"

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Choose a hosting platform:"
echo "   • Railway: https://railway.app (Recommended)"
echo "   • Render: https://render.com"
echo "   • PythonAnywhere: https://pythonanywhere.com"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"