# Employee Performance Tracker - Usage Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install openpyxl
```

### 2. Run the Script
```bash
python employee_performance_tracker.py
```

This will generate:
- `Employee_Performance_Tracker_Aug2025.xlsx` with sample data for John Doe and a clean template

## Script Features

### ✅ What the Script Creates

1. **Fully Formula-Protected Excel Workbook** with password: `secure123`
2. **Two Pre-configured Sheets:**
   - `John_Doe_Performance` - Contains realistic sample data for August 2025
   - `Template_Performance` - Clean template for new employees

3. **Automatic Calculations:**
   - Available hours based on leave status
   - Efficiency percentages
   - Performance points with complexity/QA factors
   - Bonus calculations capped at 50% of salary

4. **Data Validation & Protection:**
   - Only editable fields are unlocked
   - Dropdown validations for Y/N fields
   - Number range validations for hours/factors
   - Formula cells are completely protected

5. **Visual Formatting:**
   - Conditional highlighting for failed tasks (red)
   - Conditional highlighting for leaves (orange)
   - Conditional highlighting for high efficiency (green)
   - Professional styling with borders and alternating rows

## Adding New Employees

### Method 1: Manual (In Excel)
1. Right-click on the `Template_Performance` tab
2. Select "Move or Copy..."
3. Choose "Create a copy"
4. Rename the new tab with employee name
5. Update the Base Salary if needed
6. Start entering daily performance data

### Method 2: Programmatic
```python
from employee_performance_tracker import add_new_employee_programmatically

# Add new employee to existing file
add_new_employee_programmatically(
    "Employee_Performance_Tracker_Aug2025.xlsx", 
    "Jane_Smith", 
    year=2025, 
    month=8
)
```

## Customization Options

### Change Default Values
```python
tracker = PerformanceTracker()
tracker.base_salary = 60000  # Change default salary
tracker.password = "mypassword"  # Change protection password
```

### Different Month/Year
```python
# Generate for different month
tracker.add_employee("John_Doe", year=2025, month=9, sample_data=True)
```

### Custom Sample Data
Modify the `setup_daily_data()` method to customize:
- Meeting hours patterns
- Complexity factors
- QA factors
- Leave patterns
- Task failure rates

## File Structure Generated

```
Employee_Performance_Tracker_Aug2025.xlsx
├── John_Doe_Performance (with sample data)
└── Template_Performance (clean template)

Each sheet contains:
├── Daily tracking table (26 workdays)
│   ├── Columns A-B: Date & Day (auto-filled)
│   ├── Columns C-I: Input fields (editable)
│   └── Columns J-N: Formula columns (protected)
└── Summary section (rows 30-35)
    ├── Total points calculation
    ├── Bonus rate calculation
    └── Final pay calculation
```

## Data Types & Validation Rules

| Field | Type | Range | Validation |
|-------|------|-------|------------|
| Meeting Hrs | Decimal | 0-9 | Number validation |
| Assigned Hrs | Decimal | 1-12 | Number validation |
| Completed Hrs | Decimal | 0-16 | Number validation |
| Complexity Factor | Decimal | 0.5-3.0 | Number validation |
| QA Factor | Decimal | 0.3-2.0 | Number validation |
| Task Failed | Text | Y/N | Dropdown list |
| Leave Taken | Text | Y/N | Dropdown list |
| Base Salary | Currency | >0 | Number validation |

## Formula Reference

### Key Formulas Used:
- **Available Hours:** `=IF(Leave="Y", 0, 9-Meeting)`
- **Efficiency:** `=IF(Available=0, 0, Completed/Available)`
- **Raw Points:** `=Completed * Complexity * QA`
- **Approved Points:** `=IF(Failed="Y", 0, ROUND(Efficiency * Raw, 2))`
- **Bonus Rate:** `=(Salary * 0.5) / (Workdays * 10)`
- **Monthly Bonus:** `=MIN(Points * Rate, Salary * 0.5)`

## Troubleshooting

### Excel Protection Issues
- Use password: `secure123` to unprotect sheets
- Only input cells (columns C-I) should be editable
- If formulas are editable, protection didn't apply correctly

### Data Validation Errors
- Check that Y/N fields only contain "Y" or "N"
- Ensure numeric fields are within specified ranges
- Clear invalid data and re-enter

### Formula Calculation Issues
- Ensure Excel is set to automatic calculation
- Check for circular references
- Verify all cell references are correct

## Advanced Usage

### Batch Employee Addition
```python
employees = ["Alice_Johnson", "Bob_Wilson", "Carol_Davis"]
for emp in employees:
    tracker.add_employee(emp, sample_data=False)
```

### Custom Workday Patterns
Modify `get_workdays_for_month()` to exclude specific dates or include Sundays.

### Export to Other Formats
```python
# After generating Excel, convert to other formats
import pandas as pd
df = pd.read_excel("Employee_Performance_Tracker_Aug2025.xlsx")
df.to_csv("performance_data.csv")
```

## Integration Examples

### With Time Tracking Systems
```python
# Example: Import from time tracking API
def import_time_data(employee_name, time_data):
    # Load existing workbook
    wb = load_workbook("Employee_Performance_Tracker_Aug2025.xlsx")
    ws = wb[f"{employee_name}_Performance"]
    
    # Update cells with imported data
    for row, data in enumerate(time_data, 2):
        ws.cell(row=row, column=3, value=data['meeting_hours'])
        ws.cell(row=row, column=5, value=data['completed_hours'])
    
    wb.save("Employee_Performance_Tracker_Aug2025.xlsx")
```

### With Payroll Systems
```python
# Example: Export payroll data
def export_payroll_data():
    wb = load_workbook("Employee_Performance_Tracker_Aug2025.xlsx")
    payroll_data = []
    
    for sheet_name in wb.sheetnames:
        if "_Performance" in sheet_name:
            ws = wb[sheet_name]
            employee = sheet_name.replace("_Performance", "")
            total_pay = ws['C35'].value  # Total pay cell
            payroll_data.append({
                'employee': employee,
                'total_pay': total_pay
            })
    
    return payroll_data
```

---

## Support

For issues or customizations:
1. Check that all dependencies are installed correctly
2. Verify Excel version compatibility (Excel 2016+)
3. Ensure proper file permissions for writing
4. Review the requirements document for detailed specifications

**Generated by:** Employee Performance Tracker Generator v1.0