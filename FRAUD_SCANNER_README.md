# Fraud Content Scanner

A Streamlit application designed to detect potential financial fraud indicators in text content and web links.

## Features

- **Text Analysis**: Scans text for suspicious fraud keywords
- **Link Analysis**: Placeholder for future URL scanning capabilities
- **Risk Assessment**: Assigns Low, Medium, or High risk scores
- **Color-coded Results**: Visual risk indicators with recommendations
- **Comprehensive Database**: 24+ fraud keywords across different risk levels

## How to Use

### Running the Application

```bash
streamlit run fraud_scanner.py --server.port 8502
```

The app will open in your browser at `http://localhost:8502`

### Text Analysis

1. Select "Text Input" option
2. Paste any text content (messages, emails, social media posts)
3. Click "Analyze Text"
4. Review the risk assessment and recommendations

### Link Analysis

1. Select "URL/Link Input" option
2. Enter any web URL
3. Click "Analyze Link"
4. Current version shows placeholder (full functionality coming soon)

## Risk Assessment Levels

### High Risk 🔴 (Score: 6+)
Keywords like:
- "guaranteed returns"
- "sure shot tip"
- "IPO allotment guaranteed" 
- "doubles your money"
- "inside information"
- "100% guaranteed"
- "risk-free investment"

### Medium Risk 🟡 (Score: 3-5)
Keywords like:
- "hot tip"
- "exclusive opportunity"
- "limited time offer"
- "secret formula"
- "quick money"
- "huge returns"

### Low Risk 🟢 (Score: 1-2)
Keywords like:
- "investment opportunity"
- "high returns"
- "profitable"
- "promising stock"
- "good investment"

## Example Usage

### High Risk Example
Input: "Guaranteed 50% returns in 30 days! This is inside information about IPO allotment guaranteed. Doubles your money with no risk!"

Output: High Risk 🔴 with detailed keyword analysis

### Low Risk Example
Input: "This looks like a good investment opportunity with potential gains in the technology sector."

Output: Low Risk 🟢 with safety recommendations

## Technical Implementation

### Fraud Detection Algorithm
1. **Keyword Matching**: Case-insensitive search for predefined fraud terms
2. **Scoring System**: Each keyword has a risk value (1-3)
3. **Frequency Analysis**: Counts multiple occurrences of same keyword
4. **Risk Calculation**: Sum of (keyword_risk × frequency) for all matches

### Technology Stack
- **Frontend**: Streamlit
- **Backend Logic**: Python with pandas for data handling
- **URL Parsing**: Built-in urllib.parse
- **Text Processing**: String matching and regex

## Security Recommendations

Based on risk level, the app provides specific recommendations:

- **High Risk**: Do not invest, report to authorities
- **Medium Risk**: Exercise extreme caution, consult professionals
- **Low Risk**: Still verify independently, seek professional advice

## Future Enhancements

### Planned Features for Link Analysis
- Content extraction from web pages
- Domain reputation checking
- Website security analysis
- Phishing detection
- SSL certificate validation

### Advanced Text Analysis
- Machine learning-based sentiment analysis
- Named entity recognition for company/person mentions
- Pattern recognition for phone numbers/contact details
- Integration with known fraud databases

## Safety Disclaimer

⚠️ **Important Notes:**
- This tool is for educational and awareness purposes only
- Does not provide financial advice or investment recommendations
- Always conduct independent research and consult licensed professionals
- Report suspected fraud to SEBI, cyber crime units, or local police

## Emergency Contacts

- **SEBI Complaints**: complaints@sebi.gov.in
- **Cyber Crime Portal**: cybercrime.gov.in
- **Economic Offences Wing**: Contact local police

## Dependencies

See `requirements.txt` for full list:
- streamlit
- pandas
- numpy (for future ML features)

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run fraud_scanner.py
   ```

3. Open browser to `http://localhost:8502`

## Contributing

To add new fraud keywords or improve detection:
1. Update the `FRAUD_KEYWORDS` dictionary in `fraud_scanner.py`
2. Assign appropriate risk values (1=Low, 2=Medium, 3=High)
3. Test with sample content

## License

This project is for educational and demonstration purposes.