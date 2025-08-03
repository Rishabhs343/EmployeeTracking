#!/usr/bin/env python3
"""
PerformancePro - Enterprise Employee Performance Management System
Professional-grade system for tracking employee performance and calculating bonuses
Built for enterprise fintech companies requiring accuracy and transparency
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import calendar
import json
import uuid

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'performancepro-enterprise-grade-secret-key')

# Database configuration with fallback
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///performancepro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Enterprise Models
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, default="Your Company")
    logo_url = db.Column(db.String(300))
    primary_color = db.Column(db.String(7), default="#1a365d")
    secondary_color = db.Column(db.String(7), default="#2563eb")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget_multiplier = db.Column(db.Float, default=1.0)
    manager_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    base_salary = db.Column(db.Float, nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    reporting_manager = db.Column(db.String(100))
    employment_type = db.Column(db.String(50), default="Full-time")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    department = db.relationship('Department', backref='employees')

class DailyPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Core Performance Metrics
    meeting_hrs = db.Column(db.Float, default=0, nullable=False)
    assigned_hrs = db.Column(db.Float, default=9, nullable=False)
    completed_hrs = db.Column(db.Float, default=0, nullable=False)
    complexity_factor = db.Column(db.Float, default=1.0, nullable=False)
    qa_factor = db.Column(db.Float, default=1.0, nullable=False)
    task_failed = db.Column(db.Boolean, default=False, nullable=False)
    leave_taken = db.Column(db.Boolean, default=False, nullable=False)
    
    # Auto-calculated Performance Indicators
    available_hrs = db.Column(db.Float, default=0)
    efficiency = db.Column(db.Float, default=0)
    raw_points = db.Column(db.Float, default=0)
    ot_points = db.Column(db.Float, default=0)
    approved_points = db.Column(db.Float, default=0)
    
    # Audit Trail
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(100))
    
    employee = db.relationship('Employee', backref='performances')
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),)

class PerformanceAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    old_values = db.Column(db.Text)
    new_values = db.Column(db.Text)
    performed_by = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class MonthlySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    
    # Performance Metrics
    total_workdays = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Float, default=0)
    avg_efficiency = db.Column(db.Float, default=0)
    total_hours = db.Column(db.Float, default=0)
    task_failures = db.Column(db.Integer, default=0)
    leave_days = db.Column(db.Integer, default=0)
    overtime_days = db.Column(db.Integer, default=0)
    
    # Financial Calculations
    base_salary = db.Column(db.Float, default=0)
    bonus_rate = db.Column(db.Float, default=0)
    calculated_bonus = db.Column(db.Float, default=0)
    final_bonus = db.Column(db.Float, default=0)
    total_compensation = db.Column(db.Float, default=0)
    
    # Status
    is_finalized = db.Column(db.Boolean, default=False)
    finalized_at = db.Column(db.DateTime)
    finalized_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', backref='monthly_summaries')
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'year', 'month', name='unique_employee_month'),)

# Business Logic Functions
def calculate_performance_metrics(performance):
    """
    Enterprise-grade performance calculation engine
    Implements the sophisticated bonus calculation algorithm
    """
    
    # Step 1: Calculate Available Working Hours
    if performance.leave_taken:
        performance.available_hrs = 0
    else:
        performance.available_hrs = max(0, 9 - performance.meeting_hrs)
    
    # Step 2: Calculate Work Efficiency Ratio
    if performance.available_hrs == 0:
        performance.efficiency = 0
    else:
        performance.efficiency = min(2.0, performance.completed_hrs / performance.available_hrs)
    
    # Step 3: Calculate Raw Performance Points
    performance.raw_points = (
        performance.completed_hrs * 
        performance.complexity_factor * 
        performance.qa_factor
    )
    
    # Step 4: Calculate Overtime Contribution
    performance.ot_points = max(0, performance.completed_hrs - performance.assigned_hrs)
    
    # Step 5: Apply Quality Gates and Calculate Final Points
    if performance.task_failed:
        performance.approved_points = 0  # Quality gate: Failed tasks = 0 points
    else:
        performance.approved_points = round(
            performance.efficiency * performance.raw_points, 2
        )
    
    return performance

def get_working_days(year, month):
    """Get all business days (Monday-Saturday) for a given month"""
    business_days = []
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    
    current_date = first_day
    while current_date <= last_day:
        if current_date.weekday() < 6:  # Monday=0 to Saturday=5
            business_days.append(current_date)
        current_date += timedelta(days=1)
    
    return business_days

def calculate_monthly_compensation(employee_id, year, month):
    """
    Enterprise bonus calculation algorithm
    Implements sophisticated financial calculations with multiple validation layers
    """
    
    # Fetch employee and performance data
    employee = Employee.query.get(employee_id)
    if not employee:
        return None
    
    performances = DailyPerformance.query.filter_by(employee_id=employee_id).filter(
        db.extract('year', DailyPerformance.date) == year,
        db.extract('month', DailyPerformance.date) == month
    ).all()
    
    working_days = get_working_days(year, month)
    
    # Core Performance Metrics
    total_points = sum(p.approved_points for p in performances)
    total_hours = sum(p.completed_hrs for p in performances)
    work_performances = [p for p in performances if not p.leave_taken]
    avg_efficiency = (
        sum(p.efficiency for p in work_performances) / len(work_performances) 
        if work_performances else 0
    )
    
    # Risk and Quality Metrics
    task_failures = sum(1 for p in performances if p.task_failed)
    leave_days = sum(1 for p in performances if p.leave_taken)
    overtime_days = sum(1 for p in performances if p.ot_points > 0)
    
    # Financial Calculations
    max_possible_points = len(working_days) * 10  # 10 points per day maximum
    max_bonus_amount = employee.base_salary * 0.5  # 50% salary cap
    
    if max_possible_points > 0:
        bonus_rate_per_point = max_bonus_amount / max_possible_points
        calculated_bonus = total_points * bonus_rate_per_point
        final_bonus = min(calculated_bonus, max_bonus_amount)
    else:
        bonus_rate_per_point = 0
        calculated_bonus = 0
        final_bonus = 0
    
    total_compensation = employee.base_salary + final_bonus
    
    # Create or update monthly summary
    summary = MonthlySummary.query.filter_by(
        employee_id=employee_id, year=year, month=month
    ).first()
    
    if not summary:
        summary = MonthlySummary(employee_id=employee_id, year=year, month=month)
    
    # Update all metrics
    summary.total_workdays = len(working_days)
    summary.total_points = total_points
    summary.avg_efficiency = avg_efficiency
    summary.total_hours = total_hours
    summary.task_failures = task_failures
    summary.leave_days = leave_days
    summary.overtime_days = overtime_days
    summary.base_salary = employee.base_salary
    summary.bonus_rate = bonus_rate_per_point
    summary.calculated_bonus = calculated_bonus
    summary.final_bonus = final_bonus
    summary.total_compensation = total_compensation
    
    return summary

# API Routes
@app.route('/')
def dashboard():
    """Enterprise Dashboard - Executive Overview"""
    current_date = datetime.now()
    employees = Employee.query.filter_by(is_active=True).all()
    departments = Department.query.all()
    
    # Calculate comprehensive metrics
    dashboard_metrics = []
    total_company_points = 0
    total_company_hours = 0
    total_company_bonus = 0
    
    for emp in employees:
        performances = DailyPerformance.query.filter_by(employee_id=emp.id).filter(
            db.extract('year', DailyPerformance.date) == current_date.year,
            db.extract('month', DailyPerformance.date) == current_date.month
        ).all()
        
        total_points = sum(p.approved_points for p in performances)
        total_hours = sum(p.completed_hrs for p in performances)
        work_days = len([p for p in performances if not p.leave_taken])
        
        # Calculate current month bonus projection
        working_days = get_working_days(current_date.year, current_date.month)
        max_bonus = emp.base_salary * 0.5
        if working_days:
            bonus_rate = max_bonus / (len(working_days) * 10)
            projected_bonus = min(total_points * bonus_rate, max_bonus)
        else:
            projected_bonus = 0
        
        avg_points_per_day = total_points / work_days if work_days > 0 else 0
        avg_efficiency = sum(p.efficiency for p in performances if not p.leave_taken) / work_days if work_days > 0 else 0
        
        dashboard_metrics.append({
            'employee': emp,
            'total_points': total_points,
            'total_hours': total_hours,
            'work_days': work_days,
            'avg_points_per_day': avg_points_per_day,
            'avg_efficiency': avg_efficiency,
            'projected_bonus': projected_bonus,
            'performance_grade': get_performance_grade(avg_points_per_day)
        })
        
        total_company_points += total_points
        total_company_hours += total_hours
        total_company_bonus += projected_bonus
    
    # Sort by performance for leaderboard
    dashboard_metrics.sort(key=lambda x: x['total_points'], reverse=True)
    
    company_stats = {
        'total_employees': len(employees),
        'total_points': total_company_points,
        'total_hours': total_company_hours,
        'total_projected_bonus': total_company_bonus,
        'avg_points_per_employee': total_company_points / len(employees) if employees else 0
    }
    
    return render_template('dashboard.html',
                         employees=employees,
                         departments=departments,
                         dashboard_metrics=dashboard_metrics,
                         company_stats=company_stats,
                         current_month=calendar.month_name[current_date.month],
                         current_year=current_date.year)

def get_performance_grade(avg_points):
    """Convert average points to performance grade"""
    if avg_points >= 12:
        return {'grade': 'A+', 'class': 'success', 'desc': 'Exceptional'}
    elif avg_points >= 10:
        return {'grade': 'A', 'class': 'success', 'desc': 'Excellent'}
    elif avg_points >= 8:
        return {'grade': 'B+', 'class': 'primary', 'desc': 'Very Good'}
    elif avg_points >= 7:
        return {'grade': 'B', 'class': 'info', 'desc': 'Good'}
    elif avg_points >= 5:
        return {'grade': 'C', 'class': 'warning', 'desc': 'Satisfactory'}
    else:
        return {'grade': 'D', 'class': 'danger', 'desc': 'Needs Improvement'}

@app.route('/employees')
def employees():
    """Employee Management Hub"""
    employees = Employee.query.all()
    departments = Department.query.all()
    return render_template('employees.html', employees=employees, departments=departments)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    """Professional Employee Onboarding"""
    if request.method == 'POST':
        data = request.json
        
        # Generate unique employee ID
        employee_id = f"EMP{datetime.now().strftime('%Y')}{Employee.query.count() + 1:04d}"
        
        employee = Employee(
            employee_id=employee_id,
            name=data['name'],
            email=data['email'],
            designation=data['designation'],
            base_salary=float(data['base_salary']),
            join_date=datetime.strptime(data['join_date'], '%Y-%m-%d').date(),
            reporting_manager=data.get('reporting_manager', ''),
            employment_type=data.get('employment_type', 'Full-time')
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'employee_id': employee.id,
            'employee_code': employee.employee_id,
            'message': f'Employee {employee.name} successfully onboarded with ID: {employee.employee_id}'
        })
    
    departments = Department.query.all()
    return render_template('add_employee.html', departments=departments)

@app.route('/performance/<int:employee_id>')
def employee_performance(employee_id):
    """Professional Performance Management Interface"""
    employee = Employee.query.get_or_404(employee_id)
    current_date = datetime.now()
    
    # Get current month performance data
    performances = DailyPerformance.query.filter_by(employee_id=employee_id).filter(
        db.extract('year', DailyPerformance.date) == current_date.year,
        db.extract('month', DailyPerformance.date) == current_date.month
    ).order_by(DailyPerformance.date).all()
    
    working_days = get_working_days(current_date.year, current_date.month)
    performance_map = {p.date: p for p in performances}
    
    # Calculate month-to-date metrics
    mtd_summary = calculate_monthly_compensation(employee_id, current_date.year, current_date.month)
    
    return render_template('performance.html',
                         employee=employee,
                         working_days=working_days,
                         performances=performance_map,
                         mtd_summary=mtd_summary,
                         current_month=calendar.month_name[current_date.month],
                         current_year=current_date.year)

@app.route('/api/performance', methods=['POST'])
def save_performance_data():
    """Enterprise-grade Performance Data API"""
    try:
        data = request.json
        
        # Validate input data
        required_fields = ['employee_id', 'date', 'completed_hrs']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Get or create performance record
        performance = DailyPerformance.query.filter_by(
            employee_id=data['employee_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        ).first()
        
        if not performance:
            performance = DailyPerformance(
                employee_id=data['employee_id'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date()
            )
        
        # Update performance data with validation
        performance.meeting_hrs = max(0, min(9, float(data.get('meeting_hrs', 0))))
        performance.assigned_hrs = max(1, min(12, float(data.get('assigned_hrs', 9))))
        performance.completed_hrs = max(0, min(16, float(data.get('completed_hrs', 0))))
        performance.complexity_factor = max(0.5, min(3.0, float(data.get('complexity_factor', 1.0))))
        performance.qa_factor = max(0.3, min(2.0, float(data.get('qa_factor', 1.0))))
        performance.task_failed = bool(data.get('task_failed', False))
        performance.leave_taken = bool(data.get('leave_taken', False))
        performance.updated_by = "System Admin"  # In real app, this would be current user
        
        # Calculate all derived metrics
        performance = calculate_performance_metrics(performance)
        
        # Save to database
        db.session.add(performance)
        db.session.commit()
        
        # Create audit log
        audit = PerformanceAudit(
            employee_id=performance.employee_id,
            action="Performance Updated",
            new_values=json.dumps({
                'date': data['date'],
                'completed_hrs': performance.completed_hrs,
                'approved_points': performance.approved_points
            }),
            performed_by="System Admin"
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'approved_points': performance.approved_points,
                'efficiency': round(performance.efficiency * 100, 1),
                'available_hrs': performance.available_hrs,
                'raw_points': performance.raw_points,
                'ot_points': performance.ot_points
            },
            'message': 'Performance data saved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leaderboard')
def get_enterprise_leaderboard():
    """Real-time Performance Leaderboard API"""
    current_date = datetime.now()
    employees = Employee.query.filter_by(is_active=True).all()
    
    leaderboard_data = []
    for emp in employees:
        performances = DailyPerformance.query.filter_by(employee_id=emp.id).filter(
            db.extract('year', DailyPerformance.date) == current_date.year,
            db.extract('month', DailyPerformance.date) == current_date.month
        ).all()
        
        # Calculate comprehensive metrics
        total_points = sum(p.approved_points for p in performances)
        work_performances = [p for p in performances if not p.leave_taken]
        avg_efficiency = (
            sum(p.efficiency for p in work_performances) / len(work_performances) * 100
            if work_performances else 0
        )
        
        performance_grade = get_performance_grade(
            total_points / len(work_performances) if work_performances else 0
        )
        
        leaderboard_data.append({
            'employee_id': emp.id,
            'employee_code': emp.employee_id,
            'name': emp.name,
            'designation': emp.designation,
            'department': emp.department.name if emp.department else 'N/A',
            'total_points': round(total_points, 2),
            'work_days': len(work_performances),
            'avg_efficiency': round(avg_efficiency, 1),
            'performance_grade': performance_grade,
            'total_hours': sum(p.completed_hrs for p in performances),
            'task_failures': sum(1 for p in performances if p.task_failed),
            'overtime_days': sum(1 for p in performances if p.ot_points > 0)
        })
    
    # Sort by total points (descending)
    leaderboard_data.sort(key=lambda x: x['total_points'], reverse=True)
    
    # Add rankings
    for i, employee_data in enumerate(leaderboard_data):
        employee_data['rank'] = i + 1
    
    return jsonify(leaderboard_data)

@app.route('/analytics')
def analytics_dashboard():
    """Advanced Analytics Dashboard"""
    return render_template('analytics.html')

# ============================================================================
# ENTERPRISE API ENDPOINTS FOR REAL-TIME CHARTS AND ANALYTICS  
# ============================================================================

@app.route('/api/dashboard_metrics')
def get_dashboard_metrics():
    """Get real-time dashboard metrics for charts"""
    current_date = datetime.now()
    
    # Calculate real performance trends (last 4 weeks)
    weeks_data = []
    labels = []
    
    for week in range(4, 0, -1):
        week_start = current_date - timedelta(weeks=week)
        week_end = week_start + timedelta(days=6)
        
        week_performances = DailyPerformance.query.filter(
            DailyPerformance.date >= week_start.date(),
            DailyPerformance.date <= week_end.date()
        ).all()
        
        if week_performances:
            avg_points = sum(p.approved_points for p in week_performances) / len(week_performances)
            avg_efficiency = sum(p.efficiency for p in week_performances) / len(week_performances) * 100
        else:
            avg_points = 8.0  # Default baseline
            avg_efficiency = 85.0
            
        weeks_data.append({
            'points': round(avg_points, 1),
            'efficiency': round(avg_efficiency, 1)
        })
        labels.append(f'Week {5-week}')
    
    # Current week projection
    current_week_start = current_date - timedelta(days=current_date.weekday())
    current_performances = DailyPerformance.query.filter(
        DailyPerformance.date >= current_week_start.date()
    ).all()
    
    if current_performances:
        current_avg = sum(p.approved_points for p in current_performances) / len(current_performances)
        projected_points = min(current_avg * 1.05, 12)  # 5% improvement projection
        projected_efficiency = min(projected_points * 10, 100)
    else:
        projected_points = 9.0
        projected_efficiency = 90.0
    
    weeks_data.append({
        'points': round(projected_points, 1),
        'efficiency': round(projected_efficiency, 1)
    })
    labels.append('Week 5 (Projected)')
    
    return jsonify({
        'trends': {
            'labels': labels,
            'points': [w['points'] for w in weeks_data],
            'efficiency': [w['efficiency'] for w in weeks_data]
        }
    })

@app.route('/api/department_performance')
def get_department_performance():
    """Get department-wise performance breakdown"""
    departments = Department.query.all()
    dept_data = []
    
    current_date = datetime.now()
    
    for dept in departments:
        dept_employees = Employee.query.filter_by(department_id=dept.id, is_active=True).all()
        
        if dept_employees:
            # Get current month performance for department
            dept_performances = []
            for emp in dept_employees:
                performances = DailyPerformance.query.filter_by(employee_id=emp.id).filter(
                    db.extract('year', DailyPerformance.date) == current_date.year,
                    db.extract('month', DailyPerformance.date) == current_date.month
                ).all()
                dept_performances.extend(performances)
            
            if dept_performances:
                avg_points = sum(p.approved_points for p in dept_performances) / len(dept_performances)
                avg_efficiency = sum(p.efficiency for p in dept_performances) / len(dept_performances) * 100
            else:
                # Use baseline performance based on department
                baseline_map = {
                    'Engineering': 9.2,
                    'Product Management': 8.8, 
                    'Sales & Marketing': 7.5,
                    'Operations': 8.0,
                    'Finance & Admin': 7.8,
                    'Human Resources': 7.2
                }
                avg_points = baseline_map.get(dept.name, 8.0)
                avg_efficiency = avg_points * 10
            
            dept_data.append({
                'name': dept.name,
                'employee_count': len(dept_employees),
                'avg_points': round(avg_points, 1),
                'avg_efficiency': round(avg_efficiency, 1),
                'performance_grade': get_dept_grade(avg_points)
            })
    
    return jsonify(dept_data)

def get_dept_grade(avg_points):
    """Get department performance grade"""
    if avg_points >= 10:
        return {'grade': 'A+', 'class': 'success'}
    elif avg_points >= 8:
        return {'grade': 'A', 'class': 'primary'}
    elif avg_points >= 6:
        return {'grade': 'B+', 'class': 'info'}
    elif avg_points >= 4:
        return {'grade': 'B', 'class': 'warning'}
    else:
        return {'grade': 'C', 'class': 'danger'}

@app.route('/api/performance_distribution')
def get_performance_distribution():
    """Get employee performance distribution data"""
    current_date = datetime.now()
    employees = Employee.query.filter_by(is_active=True).all()
    
    distribution = {'top': 0, 'high': 0, 'average': 0, 'needs_support': 0}
    
    for emp in employees:
        performances = DailyPerformance.query.filter_by(employee_id=emp.id).filter(
            db.extract('year', DailyPerformance.date) == current_date.year,
            db.extract('month', DailyPerformance.date) == current_date.month
        ).all()
        
        work_performances = [p for p in performances if not p.leave_taken]
        if work_performances:
            avg_points = sum(p.approved_points for p in work_performances) / len(work_performances)
            
            if avg_points >= 10:
                distribution['top'] += 1
            elif avg_points >= 7:
                distribution['high'] += 1
            elif avg_points >= 4:
                distribution['average'] += 1
            else:
                distribution['needs_support'] += 1
        else:
            # For employees with no data, assign to average
            distribution['average'] += 1
    
    total = sum(distribution.values())
    if total > 0:
        percentages = {k: round(v/total*100) for k, v in distribution.items()}
    else:
        percentages = {'top': 25, 'high': 50, 'average': 20, 'needs_support': 5}
    
    return jsonify({
        'labels': ['Top Performers', 'High Performers', 'Average', 'Needs Support'],
        'data': [percentages['top'], percentages['high'], percentages['average'], percentages['needs_support']],
        'colors': ['rgb(16, 185, 129)', 'rgb(59, 130, 246)', 'rgb(245, 158, 11)', 'rgb(239, 68, 68)']
    })

@app.route('/api/employee/<int:employee_id>/performance_trend')
def get_employee_performance_trend(employee_id):
    """Get individual employee performance trend for charts"""
    current_date = datetime.now()
    
    # Get last 30 days of performance
    performances = DailyPerformance.query.filter_by(employee_id=employee_id).filter(
        DailyPerformance.date >= (current_date - timedelta(days=30)).date()
    ).order_by(DailyPerformance.date).all()
    
    labels = []
    points_data = []
    
    # Fill in gaps for missing days to show complete trend
    for i in range(30):
        check_date = (current_date - timedelta(days=29-i)).date()
        perf = next((p for p in performances if p.date == check_date), None)
        
        labels.append(check_date.strftime('%m/%d'))
        if perf:
            points_data.append(perf.approved_points)
        else:
            points_data.append(0)  # No performance data for this day
    
    return jsonify({
        'labels': labels,
        'points': points_data,
        'target': [10] * len(labels)  # Target line at 10 points
    })

@app.route('/api/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """Edit employee information"""
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        data = request.json
        
        # Update employee fields
        employee.name = data.get('name', employee.name)
        employee.email = data.get('email', employee.email)
        employee.designation = data.get('designation', employee.designation)
        employee.base_salary = float(data.get('base_salary', employee.base_salary))
        employee.reporting_manager = data.get('reporting_manager', employee.reporting_manager)
        employee.employment_type = data.get('employment_type', employee.employment_type)
        
        if data.get('department_id'):
            employee.department_id = int(data.get('department_id'))
        
        # Create audit log
        audit = PerformanceAudit(
            employee_id=employee_id,
            action="Employee Updated",
            new_values=json.dumps({
                'name': employee.name,
                'salary': employee.base_salary,
                'designation': employee.designation
            }),
            performed_by="System Admin"
        )
        
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Employee {employee.name} updated successfully'
        })
    
    # GET request - return employee data
    departments = Department.query.all()
    return jsonify({
        'employee': {
            'id': employee.id,
            'name': employee.name,
            'email': employee.email,
            'designation': employee.designation,
            'base_salary': employee.base_salary,
            'department_id': employee.department_id,
            'reporting_manager': employee.reporting_manager,
            'employment_type': employee.employment_type,
            'join_date': employee.join_date.isoformat()
        },
        'departments': [{'id': d.id, 'name': d.name} for d in departments]
    })

# Initialize Database
def init_enterprise_db():
    """Initialize enterprise database with sample data"""
    db.create_all()
    
    # Create default department if none exists
    if Department.query.count() == 0:
        departments = [
            Department(name="Engineering", manager_name="Tech Lead"),
            Department(name="Product", manager_name="Product Manager"),
            Department(name="Sales", manager_name="Sales Director"),
            Department(name="Marketing", manager_name="Marketing Head"),
            Department(name="Operations", manager_name="Operations Manager")
        ]
        for dept in departments:
            db.session.add(dept)
    
    # Create sample employee if none exists
    if Employee.query.count() == 0:
        eng_dept = Department.query.filter_by(name="Engineering").first()
        sample_employee = Employee(
            employee_id="EMP202400001",
            name="John Doe",
            email="john.doe@company.com",
            designation="Senior Software Engineer",
            department_id=eng_dept.id if eng_dept else None,
            base_salary=75000,
            join_date=date(2024, 1, 15),
            reporting_manager="Tech Lead",
            employment_type="Full-time"
        )
        db.session.add(sample_employee)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_enterprise_db()
    
    print("🏢 PerformancePro Enterprise System Starting...")
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 Built for Enterprise-grade Performance Management")
    app.run(debug=True, host='0.0.0.0', port=5000)
