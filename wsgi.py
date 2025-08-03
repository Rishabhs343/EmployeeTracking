#!/usr/bin/env python3
"""
WSGI Configuration for PythonAnywhere
This file configures your Flask app for PythonAnywhere hosting
"""

import sys
import os

# Add your project directory to Python path
# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/EmployeeTracking'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'performancepro-enterprise-grade-secret-key-change-in-production')

# Import your Flask application
from run import app as application

if __name__ == "__main__":
    application.run()