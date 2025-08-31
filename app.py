from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Paths to data files (CSV and Excel)
CSV_FILE_PATH = 'sebi_advisors.csv'
EXCEL_FILE_PATH = 'ia08012025.xlsx'  # Your Excel file
DATA_FILES = [EXCEL_FILE_PATH, CSV_FILE_PATH]  # Priority order: Excel first, then CSV

def load_advisors_data():
    """Load advisors data from Excel or CSV file"""
    try:
        advisors = []
        
        # Try to load from available data files in priority order
        for file_path in DATA_FILES:
            if os.path.exists(file_path):
                print(f"Found data file: {file_path}")
                
                if file_path.endswith(('.xlsx', '.xls')):
                    try:
                        # Load Excel file
                        print(f"Attempting to load Excel file: {file_path}")
                        df = pd.read_excel(file_path)
                        
                        # Convert DataFrame to list of dictionaries
                        advisors = df.to_dict('records')
                        
                        # Ensure string conversion for consistent processing
                        for advisor in advisors:
                            for key, value in advisor.items():
                                if pd.isna(value):
                                    advisor[key] = ''
                                else:
                                    advisor[key] = str(value)
                        
                        print(f"Successfully loaded {len(advisors)} advisors from Excel file")
                        print(f"Excel columns found: {list(df.columns)}")
                        return advisors
                        
                    except ImportError as e:
                        print(f"Cannot read Excel file - missing dependency: {e}")
                        print(f"Please install: pip install openpyxl")
                        print(f"Skipping Excel file and trying CSV...")
                        continue
                    except Exception as e:
                        print(f"Error reading Excel file {file_path}: {e}")
                        continue
                        
                elif file_path.endswith('.csv'):
                    try:
                        # Load CSV file
                        print(f"Loading CSV file: {file_path}")
                        with open(file_path, 'r', newline='', encoding='utf-8') as file:
                            csv_reader = csv.DictReader(file)
                            for row in csv_reader:
                                advisors.append(row)
                        
                        print(f"Successfully loaded {len(advisors)} advisors from CSV file")
                        return advisors
                    except Exception as e:
                        print(f"Error reading CSV file {file_path}: {e}")
                        continue
        
        print(f"No accessible data files found. Checked: {DATA_FILES}")
        print(f"Note: If you have an Excel file, install openpyxl: pip install openpyxl")
        return []
        
    except Exception as e:
        print(f"Error loading data file: {e}")
        return []

def is_validity_current(validity_date):
    """Check if the validity date is current (not expired)"""
    try:
        validity = datetime.strptime(validity_date, '%Y-%m-%d')
        current_date = datetime.now()
        return validity >= current_date
    except:
        return False

@app.route('/verify_advisor', methods=['POST'])
def verify_advisor():
    """
    Verify SEBI advisor by name or registration number
    Expected JSON input: {"query": "advisor_name_or_regno"}
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing query parameter in request body'
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query parameter cannot be empty'
            }), 400
        
        # Load advisors data
        advisors_data = load_advisors_data()
        
        if not advisors_data:
            return jsonify({
                'status': 'error',
                'message': 'Unable to load advisors database'
            }), 500
        
        # Search for advisor by name or registration number (case-insensitive)
        found_advisor = None
        for advisor in advisors_data:
            name_match = query.lower() in advisor['Name'].lower()
            regno_match = query.lower() == advisor['RegNo'].lower()
            if name_match or regno_match:
                found_advisor = advisor
                break
        
        if not found_advisor:
            return jsonify({
                'status': 'Not Found',
                'message': 'Advisor not found in SEBI database'
            })
        
        # Get the found advisor
        advisor = found_advisor
        
        # Check if validity is current
        is_valid = is_validity_current(advisor['Validity'])
        
        return jsonify({
            'status': 'Verified',
            'advisor_details': {
                'name': advisor['Name'],
                'registration_number': advisor['RegNo'],
                'validity': advisor['Validity'],
                'is_current': is_valid,
                'validity_status': 'Valid' if is_valid else 'Expired'
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SEBI Advisor Verification API is running'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'SEBI Advisor Verification API',
        'endpoints': {
            '/verify_advisor': 'POST - Verify advisor by name or registration number',
            '/health': 'GET - Health check'
        },
        'usage': {
            'method': 'POST',
            'endpoint': '/verify_advisor',
            'body': {'query': 'advisor_name_or_registration_number'}
        }
    })

if __name__ == '__main__':
    print("Starting SEBI Advisor Verification API...")
    print(f"Looking for data files:")
    for file_path in DATA_FILES:
        abs_path = os.path.abspath(file_path)
        exists = "✓" if os.path.exists(file_path) else "✗"
        print(f"  {exists} {abs_path}")
    
    # Test loading data
    test_data = load_advisors_data()
    print(f"Successfully loaded {len(test_data)} advisor records")
    
    app.run(debug=True, host='0.0.0.0', port=5000)