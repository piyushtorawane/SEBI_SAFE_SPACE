#!/usr/bin/env python3
"""
Convert Excel file to CSV for SEBI Advisor Verification System
"""

import pandas as pd
import os

def convert_excel_to_csv(excel_file_path, csv_output_path='sebi_advisors.csv'):
    """
    Convert Excel file to CSV format
    
    Args:
        excel_file_path (str): Path to the Excel file
        csv_output_path (str): Output CSV file path
    """
    try:
        # Read Excel file
        print(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        # Display the columns to help with mapping
        print("\nColumns found in Excel file:")
        for i, col in enumerate(df.columns):
            print(f"{i+1}. {col}")
        
        # Display first few rows
        print("\nFirst 5 rows of data:")
        print(df.head())
        
        # Expected columns for the system: Name, RegNo, Validity
        # You may need to rename columns to match the expected format
        
        # Example mapping (adjust based on your Excel structure):
        column_mapping = {
            # 'Your Excel Column Name': 'Expected Column Name'
            # Uncomment and modify the lines below based on your Excel structure
            # 'Advisor Name': 'Name',
            # 'Registration Number': 'RegNo', 
            # 'Validity Date': 'Validity'
        }
        
        # If you need to rename columns, uncomment the line below:
        # df = df.rename(columns=column_mapping)
        
        # Ensure required columns exist
        required_columns = ['Name', 'RegNo', 'Validity']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"\nWarning: Missing required columns: {missing_columns}")
            print("Please update the column_mapping dictionary in this script")
            
            # Show current columns vs required
            print(f"\nCurrent columns: {list(df.columns)}")
            print(f"Required columns: {required_columns}")
            return False
        
        # Save to CSV
        df[required_columns].to_csv(csv_output_path, index=False)
        print(f"\nSuccessfully converted to: {csv_output_path}")
        print(f"Total records: {len(df)}")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Excel file not found: {excel_file_path}")
        return False
    except Exception as e:
        print(f"Error converting Excel to CSV: {str(e)}")
        return False

if __name__ == "__main__":
    # Usage example:
    # 1. Place your Excel file in this directory
    # 2. Update the excel_file_name below
    # 3. Run: python convert_excel_to_csv.py
    
    excel_file_name = "ia08012025.xlsx"  # Your Excel file name
    
    if os.path.exists(excel_file_name):
        convert_excel_to_csv(excel_file_name)
    else:
        print(f"Please place your Excel file in the current directory and name it '{excel_file_name}'")
        print("Or update the 'excel_file_name' variable in this script")
        print("\nYour Excel file should have columns that can be mapped to:")
        print("- Name (Advisor Name)")
        print("- RegNo (Registration Number)")  
        print("- Validity (Validity Date in YYYY-MM-DD format)")