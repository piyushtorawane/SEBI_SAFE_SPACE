# BSE Corporate Announcement Analyzer

A comprehensive Python application that fetches, analyzes, and evaluates the credibility of corporate announcements from BSE India using advanced NLP techniques and historical pattern matching.

## Features

### 🔍 **Real-time Data Fetching**
- Fetches latest corporate announcements from BSE India API 
- Mock API integration for development and testing
- Fallback mechanisms for offline functionality
- Support for multiple data sources

### 📊 **Credibility Analysis Engine**
- **Historical Comparison**: Compares announcements against 6-month historical data
- **Sentiment Analysis**: Advanced keyword-based sentiment detection
- **Mismatch Detection**: Identifies contradictions in financial claims
- **Risk Scoring**: Assigns High/Medium/Low credibility levels

### 🎯 **Intelligent Detection**
- **Positive Indicators**: "record profit", "exceptional growth", "highest revenue"
- **Negative Indicators**: "massive loss", "financial crisis", "worst performance"
- **Neutral Indicators**: "board meeting", "dividend declaration", "compliance"
- **Pattern Recognition**: Detects drastic mismatches in company reporting

### 📈 **Interactive Dashboard**
- Real-time announcement feed
- Color-coded credibility badges
- Filtering by company and credibility level
- Historical data visualization
- Export functionality (CSV download)

## Technical Architecture

### Data Sources
- **Primary**: BSE India API (mock implementation for demo)
- **Backup**: RSS feeds and web scraping
- **Historical**: Local CSV database with 50+ sample records

### Analysis Components
1. **Sentiment Analyzer**: Keyword-based classification
2. **Credibility Engine**: Historical pattern matching
3. **Mismatch Detector**: Contradiction identification
4. **Risk Scorer**: Multi-factor assessment

### Technology Stack
- **Backend**: Python with requests for API integration
- **Frontend**: Streamlit for interactive dashboard
- **Data**: CSV-based historical storage
- **NLP**: Custom keyword analysis engine

## Installation & Setup

### Prerequisites
- Python 3.9+
- Streamlit
- Required packages (see requirements.txt)

### Quick Start
```bash
# Install dependencies
pip install streamlit requests

# Run the application
streamlit run announcement_analyzer.py --server.port 8503
```

### Alternative Installation
```bash
# Install all project dependencies
pip install -r requirements.txt

# Start the analyzer
streamlit run announcement_analyzer.py
```

## Usage Guide

### 1. **Dashboard Overview**
- **Summary Metrics**: Total announcements, credibility distribution
- **Real-time Feed**: Latest corporate announcements
- **Filter Controls**: Company and credibility level filters

### 2. **Fetching Announcements**
- Click "🔄 Fetch Latest Announcements" to get fresh data
- System automatically loads initial data on startup
- Handles API failures gracefully with fallback data

### 3. **Understanding Credibility Levels**

#### 🟢 **High Credibility (Score: 0.7-1.0)**
- Consistent with historical patterns
- Moderate, realistic claims
- No contradictions detected
- **Example**: "Quarterly dividend declaration approved by board"

#### 🟡 **Medium Credibility (Score: 0.4-0.69)**
- Some concerns or limited historical data
- Mixed signals in announcement
- Requires additional verification
- **Example**: "Steady growth reported amid market challenges"

#### 🔴 **Low Credibility (Score: 0.0-0.39)**
- Contradicts recent financial filings
- Extreme or unrealistic claims
- Suspicious pattern detected
- **Example**: "Record profit after 3 consecutive quarterly losses"

### 4. **Red Flag Detection**
The system automatically flags suspicious patterns:
- **Profit Claims**: Record profits after recent losses
- **Loss Claims**: Massive losses after positive trends
- **Extreme Language**: Excessive superlatives and guarantees
- **Pattern Breaks**: Sudden reversals in financial narrative

## Sample Analysis Cases

### Case 1: High Risk Detection
**Input**: "Reliance Industries reports record profit of ₹15,000 crores with exceptional growth"
**Historical Context**: Recent quarterly losses and negative sentiment
**Result**: 🔴 Low Credibility - "Claims record profit despite 3 recent negative reports"

### Case 2: Consistent Pattern
**Input**: "HDFC Bank board meeting scheduled for dividend declaration"
**Historical Context**: Regular corporate governance announcements
**Result**: 🟢 High Credibility - "Announcement appears consistent with historical pattern"

### Case 3: Mixed Signals
**Input**: "TCS announces moderate growth with cautious outlook"
**Historical Context**: Varied recent performance
**Result**: 🟡 Medium Credibility - "Mixed signals require additional verification"

## API Integration

### Mock BSE API (Current Implementation)
```python
# Endpoint simulation
MOCK_BSE_API_URL = "https://jsonplaceholder.typicode.com/posts"

# Company mapping
BSE_COMPANIES = [
    "Reliance Industries", "TCS", "HDFC Bank", 
    "Infosys", "ICICI Bank", "Hindustan Unilever"
]
```

### Real BSE API Integration (Future)
```python
# Real implementation would use
BSE_API_ENDPOINT = "https://api.bseindia.com/v1/corporate-announcements"
REQUIRED_HEADERS = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
```

## Historical Data Structure

### CSV Format
```csv
Company,Date,AnnouncementText,Sentiment
Reliance Industries,2024-02-15,Reliance reports quarterly loss...,negative
TCS,2024-02-18,TCS announces steady growth...,positive
HDFC Bank,2024-02-21,HDFC board meeting scheduled...,neutral
```

### Analysis Fields
- **Company**: BSE-listed company name
- **Date**: Announcement date (YYYY-MM-DD)
- **AnnouncementText**: Full announcement content
- **Sentiment**: Historical sentiment classification
- **CredibilityScore**: Calculated risk score (0.0-1.0)
- **CredibilityLevel**: Final assessment (High/Medium/Low)

## Advanced Features

### Pattern Recognition
- **Trend Analysis**: 5-announcement rolling window
- **Frequency Weighting**: Multiple keyword occurrences
- **Context Sensitivity**: Industry-specific terminology
- **Historical Baseline**: Company-specific benchmarking

### Export & Integration
- **CSV Export**: Full analysis results
- **API Ready**: Modular design for integration
- **Batch Processing**: Multiple announcement analysis
- **Real-time Updates**: Live data refresh

## Configuration

### Keyword Categories
```python
CREDIBILITY_KEYWORDS = {
    "positive_financial": {
        "keywords": ["record profit", "exceptional growth"],
        "weight": 3
    },
    "negative_financial": {
        "keywords": ["massive loss", "financial crisis"], 
        "weight": 3
    }
}
```

### Historical Data Management
- **Auto-creation**: Generates sample data if none exists
- **CSV Storage**: Local file-based persistence
- **Data Validation**: Ensures data integrity
- **Backup Options**: Multiple data source support

## Troubleshooting

### Common Issues
1. **API Connection Error**
   - Solution: System uses mock data automatically
   - Check internet connection for real API usage

2. **Historical Data Missing**
   - Solution: App creates sample data automatically
   - Verify `historical_announcements.csv` exists

3. **Dependency Errors**
   - Solution: Install missing packages
   - Run: `pip install streamlit requests`

### Performance Optimization
- **Caching**: Streamlit session state management
- **Lazy Loading**: On-demand data fetching
- **Memory Management**: Efficient data structures
- **Error Handling**: Graceful degradation

## Future Enhancements

### Planned Features
1. **Real BSE API Integration**
   - Official BSE data feeds
   - Authentication and rate limiting
   - Live market data correlation

2. **Advanced NLP**
   - Machine learning sentiment analysis
   - Named entity recognition
   - Context-aware processing

3. **Enhanced Analytics**
   - Time series analysis
   - Predictive modeling
   - Cross-company correlation

4. **Integration Options**
   - REST API endpoints
   - Webhook notifications
   - Database storage

## Legal Disclaimer

⚠️ **Important Notes:**
- This tool is for research and educational purposes only
- Not intended as investment advice
- Always verify information from official sources
- Consult financial professionals for investment decisions

### Data Sources
- Mock BSE API for demonstration purposes
- Historical data patterns for analysis
- Real-time simulation for testing

### Compliance
- Respects API rate limits and terms of service
- No financial recommendations provided
- Educational use case implementation

## Support & Contact

For technical support or feature requests:
- Check documentation in `FRAUD_SCANNER_README.md`
- Review code comments in source files
- Test functionality with `test_announcement_analyzer.py`

## License

This project is for educational and demonstration purposes as part of the SEBI hack project suite.
