# 🛡️ SEBI Safe Space - Unified Financial Security Toolkit

A comprehensive financial security and compliance toolkit that combines multiple verification and detection tools into a single, professional Streamlit application with SEBI branding.

## 🎯 Overview

**SEBI Safe Space** is an all-in-one financial security platform designed to protect investors and verify financial compliance. It combines four powerful tools into a unified interface:

### 🔧 **Core Features**

#### 👨‍💼 **Tab 1: SEBI Advisor Verification**
- **CSV/Excel Lookup**: Searches local SEBI advisor database
- **Name/RegNo Search**: Find advisors by name or registration number
- **Validity Check**: Displays current registration status
- **Visual Status Cards**: Clean presentation of advisor details

### 🛡️ **Tab 2: Fraud Content Scanner**
- **Text Analysis**: Scans content for financial fraud keywords
- **Risk Scoring**: High/Medium/Low risk classification
- **Keyword Detection**: Identifies specific fraud indicators
- **Safety Recommendations**: Actionable advice based on risk level

### 📊 **Tab 3: Corporate Announcement Verifier**
- **Mock Data Fetching**: Simulates BSE announcement retrieval
- **Historical Comparison**: Analyzes against past filings
- **Credibility Scoring**: Detects suspicious claims and mismatches
- **Expandable Results**: Detailed analysis for each announcement

### 🎭 **Tab 4: Deepfake Video Detection**
- **Video Upload**: Drag-and-drop interface for video files
- **Multi-format Support**: MP4, AVI, MOV, MKV, WEBM
- **Real-time Analysis**: Live processing with progress indicators
- **Risk Assessment**: Probability scoring with visual indicators

## 🚀 Quick Start Guide

### Prerequisites
```bash
# Core dependencies
pip install streamlit requests pandas openpyxl opencv-python numpy werkzeug flask flask-cors

# Or install from requirements.txt
pip install -r requirements.txt
```

### Option 1: Basic Setup (Recommended for Testing)
```bash
# Navigate to project directory
cd "C:\Users\PIYUSH TORAWANE\Documents\SEBI hack"

# Run the unified application
streamlit run sebi_safe_space.py --server.port 8505
```

### Option 2: Full Setup (With Deepfake Detection)
```bash
# Terminal 1: Start Deepfake API
cd "C:\Users\PIYUSH TORAWANE\Documents\SEBI hack"
python deepfake_api.py

# Terminal 2: Start Main Application (New window)
cd "C:\Users\PIYUSH TORAWANE\Documents\SEBI hack"
streamlit run sebi_safe_space.py --server.port 8505
```

### Access the Application
- **Main Interface**: http://localhost:8505
- **Alternative URL**: http://127.0.0.1:8505

## 📋 Application Structure

### Main Components
- **`sebi_safe_space.py`** - Unified Streamlit application
- **`deepfake_api.py`** - Flask API for video analysis (optional)
- **`sebi_advisors.csv`** - SEBI advisor database
- **`ia08012025.xlsx`** - Excel advisor database
- **`historical_announcements.csv`** - Historical data for analysis

### Sidebar Features
- **System Status**: Real-time status of all services
- **Quick Actions**: Refresh status and system health checks
- **About Information**: Feature overview and help

### Status Indicators
- **🟢 Online/Ready**: Service is available
- **🔴 Offline**: Service needs attention
- **⚠️ Warning**: Partial functionality

## 🎯 Detailed Usage Guide

### Tab 1: SEBI Advisor Verification

#### How to Use:
1. **Input**: Enter advisor name or registration number
2. **Search**: Local database lookup (CSV/Excel)
3. **Validation**: Check registration validity dates
4. **Display**: Show advisor details with status cards

#### Sample Test Data:
```
Try these searches:
- "John Smith" (should find advisor)
- "IA001234" (should find by registration)
- "Priya Sharma" (should find advisor)
- "NonExistent" (should show not found)
```

### Tab 2: Fraud Content Scanner

#### How to Use:
1. **Input**: Paste suspicious text content
2. **Analysis**: Keyword matching against fraud database
3. **Scoring**: Calculate risk score based on detected patterns
4. **Results**: Display risk level with recommendations

#### Sample Test Content:
```
High Risk Text:
"This investment guarantees 50% returns with no risk involved!"

Medium Risk Text:
"Get this exclusive opportunity with limited time offer!"

Low Risk Text:
"This looks like a good investment opportunity in technology."
```

### Tab 3: Corporate Announcement Verifier

#### How to Use:
1. **Fetch**: Click "Fetch Announcements" to load mock data
2. **Analysis**: Automatic credibility assessment
3. **Review**: Expand each announcement for detailed analysis
4. **Export**: View analysis results with credibility scores

#### Features:
- **Real-time Fetching**: Simulated BSE data retrieval
- **Historical Context**: Comparison against past filings
- **Risk Assessment**: High/Medium/Low credibility scoring

### Tab 4: Deepfake Video Detection

#### Requirements:
- **API Status**: Deepfake API must be running (green status)
- **File Types**: MP4, AVI, MOV, MKV, WEBM
- **Size Limit**: Maximum 50MB per file

#### How to Use:
1. **Check Status**: Ensure API shows "Online" in sidebar
2. **Upload**: Drag-and-drop or select video file
3. **Analyze**: Click "Analyze Video" button
4. **Results**: View fake probability and risk assessment

#### Risk Levels:
- **🟢 Low (0-30%)**: Likely authentic video
- **🟡 Medium (30-70%)**: Uncertain, needs verification
- **🔴 High (70-100%)**: Likely deepfake or manipulated

## 🔧 Technical Configuration

### Port Configuration
- **Main Application**: http://localhost:8505
- **Deepfake API**: http://localhost:5001 (optional)
- **Legacy Advisor API**: http://localhost:5000 (optional)

### Data Files Required
- **✅ Required**: `sebi_advisors.csv` - Advisor database
- **✅ Optional**: `ia08012025.xlsx` - Excel advisor data
- **✅ Optional**: `historical_announcements.csv` - Historical data

### API Dependencies
- **Standalone**: Advisor verification, fraud scanning, announcement analysis
- **Optional**: Deepfake detection (requires separate API)

### System Architecture
```
┌─────────────────────────────────────┐
│        SEBI Safe Space UI           │
│       (Streamlit - Port 8505)       │
├─────────────────────────────────────┤
│  Tab 1: Advisor Verification        │
│  Tab 2: Fraud Scanner              │
│  Tab 3: Announcement Verifier       │
│  Tab 4: Deepfake Detector          │
└─────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
┌────────▼────────┐ ┌────────▼────────┐
│  Local Data     │ │ Deepfake API    │
│  (CSV/Excel)    │ │ (Port 5001)     │
│  - Advisors     │ │ - Video Analysis│
│  - Historical   │ │ - OpenCV        │
└─────────────────┘ └─────────────────┘
```

## 🧪 Testing & Validation

### Built-in Test Suite
```bash
# Run comprehensive tests
python test_sebi_safe_space.py
```

### Manual Testing Checklist
- [ ] **Advisor Search**: Test with sample names and registration numbers
- [ ] **Fraud Detection**: Try high/medium/low risk text samples
- [ ] **Announcements**: Fetch and analyze mock corporate data
- [ ] **Video Upload**: Test deepfake detection (if API running)
- [ ] **Status Indicators**: Verify sidebar shows correct service status

### Expected Test Results
- ✅ **Advisor Verification**: Should find sample advisors
- ✅ **Fraud Scanner**: Should detect keywords and assign risk levels
- ✅ **Announcement Analyzer**: Should fetch and analyze mock data
- ⚠️ **Deepfake Detector**: Shows offline if API not running

## 🎨 UI Features

### Professional Styling
- **SEBI Branding**: Blue and green color scheme
- **Responsive Design**: Works on different screen sizes
- **Card Layout**: Clean, professional presentation
- **Color Coding**: Risk levels with visual indicators

### Interactive Elements
- **Tabbed Navigation**: Easy switching between tools
- **Expandable Sections**: Detailed analysis results
- **Progress Indicators**: Real-time processing feedback
- **Status Badges**: Visual service health indicators

### Accessibility
- **Clear Labels**: Descriptive input fields and buttons
- **Help Text**: Contextual guidance for each feature
- **Error Messages**: User-friendly error handling
- **Sample Data**: Built-in examples for testing

## 📊 Sample Data & Examples

### Advisor Verification Examples
```
Valid Advisors:
- John Smith (IA001234)
- Priya Sharma (IA005678)
- Rajesh Kumar (IA009012)
- Anita Desai (IA003456)
```

### Fraud Detection Keywords
```
High Risk (6+ score):
- "guaranteed returns"
- "sure shot tip"
- "inside information"
- "100% guaranteed"

Medium Risk (3-5 score):
- "hot tip"
- "exclusive opportunity"
- "limited time offer"
- "quick money"

Low Risk (1-2 score):
- "investment opportunity"
- "promising stock"
- "potential gains"
```

### Corporate Announcements
```
Sample Companies:
- Reliance Industries
- TCS (Tata Consultancy Services)
- HDFC Bank
- Infosys
- ICICI Bank
```

## 🛠️ Troubleshooting

### Common Issues

#### "Can't reach this page" Error
**Solution**: 
1. Ensure Streamlit is running: `streamlit run sebi_safe_space.py --server.port 8505`
2. Check correct URL: http://localhost:8505
3. Verify no firewall blocking the connection

#### Deepfake Tab Shows "Offline"
**Solution**:
1. Start deepfake API: `python deepfake_api.py`
2. Ensure OpenCV installed: `pip install opencv-python`
3. Check API runs on port 5001

#### Module Import Errors
**Solution**:
```bash
pip install streamlit requests pandas openpyxl opencv-python numpy werkzeug flask flask-cors
```

#### File Not Found Errors
**Solution**:
1. Ensure you're in correct directory: `cd "C:\Users\PIYUSH TORAWANE\Documents\SEBI hack"`
2. Verify required files exist: `sebi_advisors.csv`
3. Check file permissions

### Performance Tips
- **File Size**: Keep video files under 50MB for deepfake analysis
- **Browser**: Use Chrome or Firefox for best compatibility
- **Memory**: Close other applications for better performance
- **Network**: Disable VPN if experiencing connection issues

## 🔐 Security & Privacy

### Data Handling
- **Local Processing**: All data processed locally, no external APIs
- **No Data Storage**: Videos deleted after analysis
- **Privacy First**: No personal data transmitted or stored
- **Secure Files**: Input validation and file type checking

### Production Considerations
- **Authentication**: Add user authentication for production use
- **HTTPS**: Use secure connections in production
- **Database**: Consider database storage for larger datasets
- **Monitoring**: Add logging and monitoring for production

## 🎓 Educational Use

### Learning Objectives
- **Financial Security**: Understanding fraud detection patterns
- **Regulatory Compliance**: SEBI advisor verification process
- **AI Detection**: Deepfake and manipulation identification
- **Data Analysis**: Corporate announcement credibility assessment

### Use Cases
- **Educational**: Teaching financial security awareness
- **Research**: Analyzing fraud patterns and detection methods
- **Demonstration**: Showcasing AI-powered verification tools
- **Training**: Financial compliance and security training

## 📞 Support & Documentation

### Additional Documentation
- **`README.md`** - General project overview
- **`FRAUD_SCANNER_README.md`** - Detailed fraud detection guide
- **`BSE_ANALYZER_README.md`** - Corporate announcement analysis
- **`DEEPFAKE_DETECTOR_README.md`** - Video analysis documentation

### Getting Help
1. **Check Status**: Verify sidebar system status indicators
2. **Review Logs**: Check terminal output for error messages
3. **Test Components**: Use built-in test suite
4. **Sample Data**: Try provided example inputs

## 🏁 Conclusion

**SEBI Safe Space** provides a comprehensive, user-friendly platform for financial security verification and fraud detection. With its unified interface and professional styling, it serves as an excellent demonstration of modern financial compliance tools.

### Ready to Use!
Your application is now fully functional and ready for:
- ✅ **SEBI Advisor Verification**
- ✅ **Fraud Content Detection**
- ✅ **Corporate Announcement Analysis**
- ✅ **Deepfake Video Detection**

**Access your application at: http://localhost:8505**

---

*For educational and demonstration purposes only. Not intended as investment advice or for production financial systems without additional security measures.*