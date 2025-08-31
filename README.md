# 🛡️ SEBI Safe Space - Unified Financial Security Toolkit

A comprehensive, unified financial security and compliance platform that combines SEBI advisor verification, fraud content detection, corporate announcement analysis, and deepfake video detection into a single, professional Streamlit application.

## 🎯 **NEW: Unified Application Available!**

**Quick Start:** `streamlit run sebi_safe_space.py --server.port 8505`

**Main Features:**
- 👨‍💼 **SEBI Advisor Verification** - CSV/Excel database lookup
- 🛡️ **Fraud Content Scanner** - Text analysis with risk scoring
- 📊 **Corporate Announcement Verifier** - Credibility analysis
- 🎭 **Deepfake Video Detection** - AI-powered video analysis

> **📖 See [SEBI_SAFE_SPACE_README.md](SEBI_SAFE_SPACE_README.md) for detailed usage guide**

## 🚀 **Quick Access URLs**

### Unified Application (Recommended)
- **SEBI Safe Space**: http://localhost:8505
- **Command**: `streamlit run sebi_safe_space.py --server.port 8505`
- **Features**: All tools in one interface with professional UI

### Individual Applications (Legacy)
- **SEBI Verification**: http://localhost:8501 (`streamlit run frontend.py --server.port 8501`)
- **Fraud Scanner**: http://localhost:8502 (`streamlit run fraud_scanner.py --server.port 8502`) 
- **BSE Analyzer**: http://localhost:8503 (`streamlit run announcement_analyzer.py --server.port 8503`)
- **Deepfake Detector**: http://localhost:8504 (`streamlit run deepfake_detector.py --server.port 8504`)

### Backend APIs (Optional)
- **Advisor API**: http://localhost:5000 (`python app.py`)
- **Deepfake API**: http://localhost:5001 (`python deepfake_api.py`)

---

# Legacy Documentation

*The following sections document the individual applications. For the unified experience, use the SEBI Safe Space application above.*

### SEBI Advisor Verification
- **Flask Backend**: REST API with `/verify_advisor` endpoint
- **Streamlit Frontend**: User-friendly web interface
- **CSV/Excel Database**: Local storage of advisor information
- **Real-time Verification**: Check advisor name or registration number
- **Validity Check**: Verify if advisor registration is current or expired

### Fraud Content Scanner 🛡️
- **Text Analysis**: Scans content for financial fraud keywords
- **Link Analysis**: URL validation and future scanning capabilities
- **Risk Assessment**: Low/Medium/High risk scoring
- **Color-coded Results**: Visual risk indicators
- **Safety Recommendations**: Actionable advice based on risk level

### BSE Announcement Analyzer 📊
- **Real-time Fetching**: Corporate announcements from BSE India API
- **Historical Comparison**: Pattern matching against past filings
- **Credibility Scoring**: Detects mismatches and suspicious claims
- **Interactive Dashboard**: Filterable analysis with export options
- **Mismatch Detection**: Flags contradictory financial statements

### Deepfake Video Detection 🎭
- **Advanced Analysis**: Multi-method deepfake detection using OpenCV
- **Real-time Processing**: Upload and analyze videos instantly
- **Risk Assessment**: Probability scoring (0-100%) with visual indicators
- **Detailed Reports**: Face consistency, temporal analysis, and AI classification
- **Secure Processing**: Local analysis with automatic file cleanup

## Files Structure

```
SEBI hack/
├── app.py                          # Flask backend application
├── frontend.py                     # Streamlit SEBI verification frontend
├── fraud_scanner.py                # Streamlit fraud detection app
├── announcement_analyzer.py        # BSE announcement credibility analyzer
├── deepfake_api.py                 # Flask deepfake detection API
├── deepfake_detector.py            # Streamlit deepfake detection frontend
├── bse_data_fetcher.py             # BSE API integration module
├── sebi_advisors.csv               # CSV database with advisor information
├── ia08012025.xlsx                 # Excel database (user's advisor data)
├── historical_announcements.csv    # Historical announcement data
├── uploads/                        # Temporary video upload directory
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── FRAUD_SCANNER_README.md         # Fraud scanner documentation
├── BSE_ANALYZER_README.md          # BSE analyzer documentation
└── DEEPFAKE_DETECTOR_README.md     # Deepfake detector documentation
```

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Applications

### Step 1: Start the Flask Backend (for SEBI Verification)

Open a terminal and run:
```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### Step 2: Start the SEBI Verification Frontend

Open a **new terminal** and run:
```bash
streamlit run frontend.py --server.port 8501
```

The SEBI verification app will open at `http://localhost:8501`

### Step 3: Start the Fraud Content Scanner (Optional)

Open a **third terminal** and run:
```bash
streamlit run fraud_scanner.py --server.port 8502
```

The fraud scanner will open at `http://localhost:8502`

### Step 4: Start the BSE Announcement Analyzer (Optional)

Open a **fourth terminal** and run:
```bash
streamlit run announcement_analyzer.py --server.port 8503
```

The BSE announcement analyzer will open at `http://localhost:8503`

### Step 5: Start the Deepfake Detection System (Optional)

Open a **fifth terminal** for the API:
```bash
python deepfake_api.py
```

The deepfake API will start on `http://localhost:5001`

Open a **sixth terminal** for the frontend:
```bash
streamlit run deepfake_detector.py --server.port 8504
```

The deepfake detector will open at `http://localhost:8504`

## API Usage

### Endpoint: `/verify_advisor`

**Method**: POST  
**URL**: `http://localhost:5000/verify_advisor`

**Request Body**:
```json
{
  "query": "advisor_name_or_registration_number"
}
```

**Response Examples**:

**Found and Verified**:
```json
{
  "status": "Verified",
  "advisor_details": {
    "name": "John Smith",
    "registration_number": "IA001234",
    "validity": "2025-12-31",
    "is_current": true,
    "validity_status": "Valid"
  }
}
```

**Not Found**:
```json
{
  "status": "Not Found",
  "message": "Advisor not found in SEBI database"
}
```

### Other Endpoints

- **GET** `/health` - Health check
- **GET** `/` - API information

## Sample Data

The `sebi_advisors.csv` file contains sample advisor data:

| Name | RegNo | Validity |
|------|--------|----------|
| John Smith | IA001234 | 2025-12-31 |
| Priya Sharma | IA005678 | 2026-06-15 |
| Rajesh Kumar | IA009012 | 2025-08-20 |
| ... | ... | ... |

## Frontend Features

- **Search Input**: Enter advisor name or registration number
- **Real-time Results**: Instant verification response
- **Status Display**: Clear indication of verification status
- **Validity Check**: Shows if registration is current or expired
- **Error Handling**: User-friendly error messages
- **Sample Data**: Built-in examples for testing

## Testing

### Test with Sample Data

Try searching for:
- **By Name**: "John Smith", "Priya", "Rajesh Kumar"
- **By RegNo**: "IA001234", "IA005678", "IA009012"

### API Testing with curl

```bash
# Test verification
curl -X POST http://localhost:5000/verify_advisor \
  -H "Content-Type: application/json" \
  -d '{"query": "John Smith"}'

# Test health endpoint
curl http://localhost:5000/health
```

## Customization

### Adding More Advisors

Edit `sebi_advisors.csv` and add new rows with:
- **Name**: Advisor's full name
- **RegNo**: Registration number (format: IA followed by numbers)
- **Validity**: Expiry date (format: YYYY-MM-DD)

### Modifying the Frontend

Edit `frontend.py` to customize:
- UI layout and styling
- Search functionality
- Display format
- Additional features

### Extending the Backend

Edit `app.py` to add:
- New API endpoints
- Enhanced search logic
- Database integration
- Authentication

## Troubleshooting

### Common Issues

1. **API Connection Error**
   - Make sure Flask server is running on port 5000
   - Check firewall settings

2. **CSV File Not Found**
   - Ensure `sebi_advisors.csv` is in the same directory as `app.py`

3. **Module Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`

4. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Update frontend URL accordingly

## Fraud Content Scanner Usage

### Text Analysis
Paste any text content to scan for fraud indicators:
- **High Risk**: "guaranteed returns", "sure shot tip", "inside information"
- **Medium Risk**: "hot tip", "exclusive opportunity", "limited time offer"
- **Low Risk**: "investment opportunity", "promising stock"

### Example Fraud Text
```
Guaranteed 50% returns in 30 days! This is inside information 
about IPO allotment guaranteed. Doubles your money with no risk!
```
**Result**: High Risk 🔴 with detailed analysis

### Link Analysis
Currently shows placeholder - future versions will include:
- Website content extraction
- Domain reputation checking
- Phishing detection

## Deepfake Video Detection Usage

### Video Analysis
Upload video files to detect potential deepfake manipulation:
- **Supported Formats**: MP4, AVI, MOV, MKV, WEBM
- **File Size Limit**: 50MB maximum
- **Analysis Methods**: Facial consistency, temporal patterns, AI classification

### Risk Assessment
- **🟢 Low Risk (0-30%)**: Likely authentic video
- **🟡 Medium Risk (30-70%)**: Mixed signals, requires verification
- **🔴 High Risk (70-100%)**: Strong deepfake indicators detected

### Example Analysis
```
Upload: suspicious_video.mp4
Result: 85% fake probability (High Risk)
Reasons: Facial inconsistencies, irregular temporal patterns
```

## License

This project is for educational and demonstration purposes.