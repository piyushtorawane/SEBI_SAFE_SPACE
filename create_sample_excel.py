#!/usr/bin/env python3
"""
Create a sample Excel file with SEBI advisor data
"""

import pandas as pd

def create_sample_excel():
    """Create a sample Excel file with advisor data"""
    
    # Sample advisor data
    advisors_data = [
        {"Name": "John Smith", "RegNo": "IA001234", "Validity": "2025-12-31"},
        {"Name": "Priya Sharma", "RegNo": "IA005678", "Validity": "2026-06-15"},
        {"Name": "Rajesh Kumar", "RegNo": "IA009012", "Validity": "2025-08-20"},
        {"Name": "Anita Desai", "RegNo": "IA003456", "Validity": "2025-11-30"},
        {"Name": "Sanjay Gupta", "RegNo": "IA007890", "Validity": "2026-03-15"},
        {"Name": "Meera Patel", "RegNo": "IA004567", "Validity": "2025-09-10"},
        {"Name": "Vikram Singh", "RegNo": "IA008901", "Validity": "2026-01-25"},
        {"Name": "Kavita Reddy", "RegNo": "IA002345", "Validity": "2025-10-05"},
        {"Name": "Amit Verma", "RegNo": "IA006789", "Validity": "2026-04-12"},
        {"Name": "Neha Joshi", "RegNo": "IA001890", "Validity": "2025-12-18"},
        # Add some expired advisors for testing
        {"Name": "Ravi Expired", "RegNo": "IA999001", "Validity": "2024-01-15"},
        {"Name": "Sunita Old", "RegNo": "IA999002", "Validity": "2023-12-31"},
    ]
    
    # Create DataFrame
    df = pd.DataFrame(advisors_data)
    
    # Save to Excel
    excel_filename = "sebi_advisors.xlsx"
    df.to_excel(excel_filename, index=False, sheet_name="SEBI_Advisors")
    
    print(f"Sample Excel file created: {excel_filename}")
    print(f"Total advisors: {len(advisors_data)}")
    print("\nColumns in the Excel file:")
    for col in df.columns:
        print(f"- {col}")
    
    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))
    
    return excel_filename

if __name__ == "__main__":
    create_sample_excel()