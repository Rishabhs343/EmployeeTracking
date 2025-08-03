# MySQL Configuration for PlanetScale
# Add this to requirements.txt: PyMySQL==1.1.0

import os
from urllib.parse import quote_plus

def get_mysql_connection_string():
    """Get MySQL connection string for PlanetScale"""
    host = os.environ.get('MYSQL_HOST')
    username = os.environ.get('MYSQL_USERNAME') 
    password = os.environ.get('MYSQL_PASSWORD')
    database = os.environ.get('MYSQL_DATABASE')
    
    if all([host, username, password, database]):
        # URL encode password to handle special characters
        password_encoded = quote_plus(password)
        return f"mysql+pymysql://{username}:{password_encoded}@{host}/{database}?ssl_disabled=true"
    
    return None

# Usage in app.py:
"""
from database_mysql import get_mysql_connection_string

# Database configuration with multiple fallbacks
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    database_url = get_mysql_connection_string()
if not database_url:
    database_url = 'sqlite:///performancepro.db'

if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
"""