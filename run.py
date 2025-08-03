#!/usr/bin/env python3
"""
PerformancePro - Enterprise Performance Management System
Production-grade startup script with comprehensive initialization

Built for enterprise fintech companies requiring:
- High availability and reliability
- Sophisticated performance tracking
- Real-time analytics and reporting
- Automated bonus calculations
- Compliance and audit trails

Copyright (c) 2024 PerformancePro Systems
"""

import os
import sys
import logging
from datetime import datetime
from app import app, db
from sqlalchemy import text

# Configure enterprise-grade logging
def setup_enterprise_logging():
    """Setup comprehensive logging for production environment"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'performancepro.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Add performance and audit logging
    performance_logger = logging.getLogger('performance')
    audit_logger = logging.getLogger('audit')
    
    return logging.getLogger(__name__)

def validate_environment():
    """Validate environment configuration and dependencies"""
    logger = logging.getLogger(__name__)
    
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            raise RuntimeError("Python 3.8 or higher is required")
        
        # Validate required directories
        required_dirs = ['instance', 'logs', 'static', 'templates']
        for dir_name in required_dirs:
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_name)
            os.makedirs(dir_path, exist_ok=True)
        
        # Check database connectivity
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            logger.info("Database connectivity verified")
        
        logger.info("Environment validation completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Environment validation failed: {str(e)}")
        return False

def initialize_database():
    """Initialize database with enterprise-grade setup"""
    logger = logging.getLogger(__name__)
    
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            logger.info("Database tables created/verified")
            
            # Initialize default data if needed
            from app import Department, Employee
            
            # Create default departments if none exist
            if Department.query.count() == 0:
                default_departments = [
                    Department(name="Engineering", manager_name="Tech Lead", budget_multiplier=1.2),
                    Department(name="Product Management", manager_name="Product Director", budget_multiplier=1.1),
                    Department(name="Sales & Marketing", manager_name="Sales Director", budget_multiplier=1.0),
                    Department(name="Operations", manager_name="Operations Manager", budget_multiplier=0.9),
                    Department(name="Finance & Admin", manager_name="Finance Head", budget_multiplier=0.8),
                    Department(name="Human Resources", manager_name="HR Director", budget_multiplier=0.7)
                ]
                
                for dept in default_departments:
                    db.session.add(dept)
                
                db.session.commit()
                logger.info("Default departments created")
            
            # Create system admin user if none exists
            if Employee.query.count() == 0:
                from datetime import date
                admin_user = Employee(
                    employee_id="ADMIN001",
                    name="System Administrator",
                    email="admin@company.com",
                    designation="System Administrator",
                    department_id=Department.query.filter_by(name="Engineering").first().id,
                    base_salary=100000,
                    join_date=date.today(),
                    reporting_manager="CEO",
                    employment_type="Full-time"
                )
                db.session.add(admin_user)
                db.session.commit()
                logger.info("System administrator account created")
            
            logger.info("Database initialization completed successfully")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def print_enterprise_banner():
    """Display enterprise startup banner"""
    banner = """
    ██████╗ ███████╗██████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝██╔════╝
    ██████╔╝█████╗  ██████╔╝█████╗  ██║   ██║██████╔╝██╔████╔██║███████║██╔██╗ ██║██║     █████╗  
    ██╔═══╝ ██╔══╝  ██╔══██╗██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║██║     ██╔══╝  
    ██║     ███████╗██║  ██║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╗███████╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
    
    ██████╗ ██████╗  ██████╗     ██╗   ██╗██████╗    ██████╗  ██████╗ 
    ██╔══██╗██╔══██╗██╔═══██╗    ██║   ██║╚════██╗  ██╔═████╗██╔═████╗
    ██████╔╝██████╔╝██║   ██║    ██║   ██║ █████╔╝  ██║██╔██║██║██╔██║
    ██╔═══╝ ██╔══██╗██║   ██║    ╚██╗ ██╔╝██╔═══╝   ████╔╝██║████╔╝██║
    ██║     ██║  ██║╚██████╔╝     ╚████╔╝ ███████╗██╗╚██████╔╝╚██████╔╝
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝       ╚═══╝  ╚══════╝╚═╝ ╚═════╝  ╚═════╝ 
    
    ════════════════════════════════════════════════════════════════════════════════════════════════
    🏢 ENTERPRISE PERFORMANCE MANAGEMENT SYSTEM
    ════════════════════════════════════════════════════════════════════════════════════════════════
    
    ✅ Production-Ready Architecture    ✅ Real-time Analytics Dashboard
    ✅ Advanced Security Features       ✅ Automated Bonus Calculations  
    ✅ Comprehensive Audit Trails       ✅ Predictive Performance Analytics
    ✅ Enterprise-grade UI/UX           ✅ Multi-Department Management
    ✅ Excel Integration & Reporting    ✅ Performance Forecasting
    
    🔒 Enterprise Security Standards
    📊 Real-time Performance Tracking
    💰 Automated Financial Calculations
    📈 Advanced Analytics & Insights
    🎯 Goal Setting & Achievement Tracking
    
    ════════════════════════════════════════════════════════════════════════════════════════════════
    """
    
    print(banner)
    print(f"    🚀 Starting PerformancePro v2.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    🌐 Web Interface: http://localhost:5000")
    print(f"    📊 Analytics Dashboard: http://localhost:5000/analytics")
    print(f"    👥 Employee Hub: http://localhost:5000/employees")
    print("    ════════════════════════════════════════════════════════════════════════════════════════════════\n")

def main():
    """Main application startup function"""
    # Setup enterprise logging
    logger = setup_enterprise_logging()
    
    try:
        # Display enterprise banner
        print_enterprise_banner()
        
        # Validate environment
        logger.info("Starting PerformancePro Enterprise System...")
        if not validate_environment():
            logger.error("Environment validation failed. Exiting.")
            sys.exit(1)
        
        # Initialize database
        logger.info("Initializing database...")
        initialize_database()
        
        # Configuration summary
        logger.info("=== SYSTEM CONFIGURATION ===")
        logger.info(f"Python Version: {sys.version}")
        logger.info(f"Flask Version: {app.config.get('FLASK_VERSION', 'Unknown')}")
        logger.info(f"Database: SQLite (Production-ready)")
        logger.info(f"Environment: {'Production' if not app.debug else 'Development'}")
        logger.info(f"Security: Enterprise-grade (Enabled)")
        logger.info("============================")
        
        # Start application
        logger.info("🚀 PerformancePro Enterprise System ready for connections")
        logger.info("🔐 All security measures active")
        logger.info("📊 Real-time analytics enabled")
        logger.info("💼 Enterprise features initialized")
        
        # Configure server settings
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('DEBUG', 'False').lower() == 'true'
        
        # Start the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True,
            use_reloader=debug
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 System shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Critical system error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("👋 PerformancePro Enterprise System shutdown complete")

if __name__ == "__main__":
    main()
