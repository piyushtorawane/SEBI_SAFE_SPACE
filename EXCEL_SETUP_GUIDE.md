# How to Add Excel File to SEBI Advisor Verification System

## Quick Summary
Your system now supports both Excel (.xlsx) and CSV files! Here's how to add your advisor Excel file:

## Method 1: Direct Excel Support (Recommended)

### Step 1: Install Required Dependency
```bash
pip install openpyxl
```

### Step 2: Prepare Your Excel File
Your Excel file should have these **exact column names**:
- **Name** - Full name of the advisor
- **RegNo** - Registration number (e.g., IA001234)  
- **Validity** - Validity date in YYYY-MM-DD format (e.g., 2025-12-31)

### Step 3: Add Your Excel File
1. Name your Excel file: `sebi_advisors.xlsx`
2. Place it in the project directory: `c:\Users\PIYUSH TORAWANE\Documents\SEBI hack\`

### Step 4: Run the System
The system will automatically detect and use your Excel file!

```bash
# Start the backend
python app.py

# Start the frontend (in new terminal)
streamlit run frontend.py
```

## Method 2: Convert Excel to CSV

If you prefer to keep using CSV or have formatting issues:

### Step 1: Run the Conversion Script
```bash
python convert_excel_to_csv.py
```

### Step 2: Update Column Mapping
Edit `convert_excel_to_csv.py` to match your Excel column names:

```python
column_mapping = {
    'Your Excel Column Name': 'Name',
    'Your RegNo Column': 'RegNo', 
    'Your Date Column': 'Validity'
}
```

## Excel File Format Requirements

### Required Columns:
| Name | RegNo | Validity |
|------|--------|----------|
| John Smith | IA001234 | 2025-12-31 |
| Priya Sharma | IA005678 | 2026-06-15 |

### Important Notes:
- **Name**: Full advisor name (any format)
- **RegNo**: Must start with "IA" followed by numbers
- **Validity**: Date in YYYY-MM-DD format
- **No extra spaces** in column headers
- **First row** should contain column headers

## Troubleshooting

### If Excel file is not detected:
1. Check file name is exactly: `sebi_advisors.xlsx`
2. Verify file is in correct directory
3. Check column names match exactly: Name, RegNo, Validity

### If you get import errors:
```bash
pip install pandas openpyxl
```

### If dates are not recognized:
- Format dates as: YYYY-MM-DD (e.g., 2025-12-31)
- In Excel, format the date column as "Text" or use the exact format above

## File Priority
The system checks files in this order:
1. `sebi_advisors.xlsx` (Excel file) - **First Priority**
2. `sebi_advisors.csv` (CSV file) - **Fallback**

If both exist, Excel takes priority.

## Test Your Setup
After adding your Excel file, you can test by:
1. Running the Flask backend
2. Checking the startup messages - it will show which file was loaded
3. Testing with sample data from your Excel file

## Need Help?
- Check the console output when starting `python app.py` - it shows which file was loaded
- Make sure column names are exactly: Name, RegNo, Validity (case-sensitive)
- Ensure date format is YYYY-MM-DD