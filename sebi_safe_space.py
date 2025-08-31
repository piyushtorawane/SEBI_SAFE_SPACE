import streamlit as st
import requests
import json
import csv
import os
import tempfile
from datetime import datetime, timedelta
import re
from typing import List, Dict, Tuple
import time

# Page Configuration
st.set_page_config(
    page_title="SEBI Safe Space",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for consistent theming
def load_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --sebi-primary: #1f4e79;
        --sebi-secondary: #2e8b57;
        --sebi-accent: #ff6b35;
        --sebi-success: #28a745;
        --sebi-warning: #ffc107;
        --sebi-danger: #dc3545;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--sebi-primary), var(--sebi-secondary));
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f4;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--sebi-primary);
        color: white;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--sebi-primary);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .status-high { background-color: var(--sebi-success); color: white; }
    .status-medium { background-color: var(--sebi-warning); color: black; }
    .status-low { background-color: var(--sebi-danger); color: white; }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--sebi-primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: var(--sebi-secondary);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-top: 2rem;
        color: #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration URLs
ADVISOR_API_URL = "http://localhost:5000"
DEEPFAKE_API_URL = "http://localhost:5001"

# ===============================
# ADVISOR VERIFICATION FUNCTIONS
# ===============================

def load_advisors_data():
    """Load advisors data from CSV files"""
    csv_files = ['sebi_advisors.csv', 'ia08012025.xlsx']
    advisors = []
    
    for file_path in csv_files:
        if os.path.exists(file_path):
            if file_path.endswith('.csv'):
                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as file:
                        csv_reader = csv.DictReader(file)
                        for row in csv_reader:
                            advisors.append(row)
                    break
                except Exception as e:
                    st.error(f"Error loading {file_path}: {e}")
            elif file_path.endswith(('.xlsx', '.xls')):
                try:
                    import pandas as pd
                    df = pd.read_excel(file_path)
                    advisors = df.to_dict('records')
                    break
                except ImportError:
                    st.warning("pandas/openpyxl not available for Excel files")
                except Exception as e:
                    st.error(f"Error loading {file_path}: {e}")
    
    return advisors

def verify_advisor_local(query):
    """Verify advisor using local data"""
    advisors_data = load_advisors_data()
    
    if not advisors_data:
        return None
    
    # Search for advisor
    for advisor in advisors_data:
        name_match = query.lower() in advisor.get('Name', '').lower()
        regno_match = query.lower() == advisor.get('RegNo', '').lower()
        if name_match or regno_match:
            # Check validity
            try:
                validity_date = datetime.strptime(advisor.get('Validity', ''), '%Y-%m-%d')
                is_current = validity_date >= datetime.now()
                
                return {
                    'status': 'Verified',
                    'advisor_details': {
                        'name': advisor.get('Name', ''),
                        'registration_number': advisor.get('RegNo', ''),
                        'validity': advisor.get('Validity', ''),
                        'is_current': is_current,
                        'validity_status': 'Valid' if is_current else 'Expired'
                    }
                }
            except:
                return {
                    'status': 'Verified',
                    'advisor_details': {
                        'name': advisor.get('Name', ''),
                        'registration_number': advisor.get('RegNo', ''),
                        'validity': advisor.get('Validity', ''),
                        'is_current': True,
                        'validity_status': 'Valid'
                    }
                }
    
    return {
        'status': 'Not Found',
        'message': 'Advisor not found in SEBI database'
    }

# ==============================
# FRAUD SCANNER FUNCTIONS
# ==============================

FRAUD_KEYWORDS = {
    "high_risk": {
        "keywords": ["guaranteed returns", "sure shot tip", "ipo allotment guaranteed", "doubles your money", 
                    "inside information", "100% guaranteed", "risk-free investment", "instant profit"],
        "weight": 3
    },
    "medium_risk": {
        "keywords": ["hot tip", "exclusive opportunity", "limited time offer", "act now", 
                    "secret formula", "quick money", "huge returns", "urgent investment"],
        "weight": 2
    },
    "low_risk": {
        "keywords": ["investment opportunity", "high returns", "profitable", "promising stock", 
                    "good investment", "market tip"],
        "weight": 1
    }
}

def analyze_fraud_content(text):
    """Analyze text for fraud indicators"""
    if not text:
        return {"risk_score": 0, "risk_level": "Low", "detected_keywords": []}
    
    text_lower = text.lower()
    detected_keywords = []
    total_risk_score = 0
    
    for category, data in FRAUD_KEYWORDS.items():
        for keyword in data["keywords"]:
            if keyword.lower() in text_lower:
                count = text_lower.count(keyword.lower())
                detected_keywords.append({
                    "keyword": keyword,
                    "category": category,
                    "weight": data["weight"],
                    "count": count
                })
                total_risk_score += data["weight"] * count
    
    # Determine risk level
    if total_risk_score >= 6:
        risk_level = "High"
    elif total_risk_score >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return {
        "risk_score": total_risk_score,
        "risk_level": risk_level,
        "detected_keywords": detected_keywords
    }

# ====================================
# ANNOUNCEMENT ANALYZER FUNCTIONS
# ====================================

def load_historical_announcements():
    """Load historical announcements data"""
    try:
        historical_data = []
        if os.path.exists('historical_announcements.csv'):
            with open('historical_announcements.csv', 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    historical_data.append(row)
        return historical_data
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
        return []

def fetch_mock_announcements():
    """Fetch mock corporate announcements"""
    companies = ["Reliance Industries", "TCS", "HDFC Bank", "Infosys", "ICICI Bank"]
    announcements = []
    
    for i, company in enumerate(companies):
        announcement_templates = [
            f"{company} reports record profit of ₹{1000+i*100} crores in Q{(i%4)+1}",
            f"{company} announces steady growth with revenue increase",
            f"{company} board approves dividend declaration",
        ]
        
        announcements.append({
            "Company": company,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "AnnouncementText": announcement_templates[i % len(announcement_templates)],
            "Source": "Mock Data"
        })
    
    return announcements

def analyze_announcement_credibility(company, announcement_text, historical_data):
    """Analyze announcement credibility against historical data"""
    # Simple credibility analysis
    company_history = [item for item in historical_data if item.get("Company") == company]
    
    # Basic scoring based on keywords and history
    positive_keywords = ["profit", "growth", "increase", "success", "strong"]
    negative_keywords = ["loss", "decline", "challenge", "difficult", "crisis"]
    
    positive_score = sum(1 for keyword in positive_keywords if keyword in announcement_text.lower())
    negative_score = sum(1 for keyword in negative_keywords if keyword in announcement_text.lower())
    
    if len(company_history) < 3:
        credibility = "Medium"
        reason = "Limited historical data for comparison"
        score = 0.5
    elif positive_score > negative_score:
        credibility = "High"
        reason = "Positive announcement with historical context"
        score = 0.8
    elif negative_score > positive_score:
        credibility = "Medium"
        reason = "Negative indicators detected"
        score = 0.4
    else:
        credibility = "High"
        reason = "Neutral announcement, consistent pattern"
        score = 0.7
    
    return credibility, reason, score

# ===============================
# DEEPFAKE DETECTION FUNCTIONS
# ===============================

def check_deepfake_api():
    """Check if deepfake API is available"""
    try:
        response = requests.get(f"{DEEPFAKE_API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_video_deepfake(video_file):
    """Analyze video for deepfake detection"""
    try:
        files = {'video': (video_file.name, video_file.getvalue(), 'video/mp4')}
        response = requests.post(f"{DEEPFAKE_API_URL}/analyze_video", files=files, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API Error: {response.status_code}', 'status': 'error'}
    except Exception as e:
        return {'error': str(e), 'status': 'error'}

# ===============================
# MAIN APPLICATION
# ===============================

def main():
    # Load CSS
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ SEBI Safe Space</h1>
        <p>Comprehensive Financial Security & Compliance Toolkit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        
        # Quick Stats
        st.markdown("### 📊 System Status")
        
        # Check API statuses
        advisor_status = "🟢 Online" if os.path.exists('sebi_advisors.csv') else "🔴 Offline"
        deepfake_status = "🟢 Online" if check_deepfake_api() else "🔴 Offline"
        
        st.markdown(f"""
        - **Advisor Verification**: {advisor_status}
        - **Fraud Scanner**: 🟢 Ready
        - **Announcement Analyzer**: 🟢 Ready
        - **Deepfake Detector**: {deepfake_status}
        """)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        st.markdown("---")
        
        # About
        st.markdown("### ℹ️ About")
        st.markdown("""
        **SEBI Safe Space** is a comprehensive toolkit for financial security and compliance verification.
        
        **Features:**
        - SEBI Advisor Verification
        - Fraud Content Detection
        - Corporate Announcement Analysis
        - Deepfake Video Detection
        """)
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👨‍💼 Advisor Verification", 
        "🛡️ Fraud Scanner", 
        "📊 Announcement Verifier",
        "🎭 Deepfake Detector"
    ])
    
    # ===============================
    # TAB 1: ADVISOR VERIFICATION
    # ===============================
    with tab1:
        st.header("👨‍💼 SEBI Advisor Verification")
        st.markdown("Verify if an investment advisor is registered with SEBI and check their validity status.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            query = st.text_input(
                "🔍 Enter Advisor Name or Registration Number:",
                placeholder="e.g., John Smith or IA001234",
                help="You can enter a partial name or exact registration number"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            verify_button = st.button("🔍 Verify Advisor", type="primary", key="verify_advisor")
        
        if verify_button and query:
            with st.spinner("Verifying advisor..."):
                result = verify_advisor_local(query.strip())
                
                if result and result['status'] == 'Verified':
                    advisor = result['advisor_details']
                    
                    st.success("✅ **Advisor Found and Verified!**")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>👤 Advisor Details</h4>
                            <p><strong>Name:</strong> {advisor['name']}</p>
                            <p><strong>Registration:</strong> {advisor['registration_number']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>📅 Validity</h4>
                            <p><strong>Valid Until:</strong> {advisor['validity']}</p>
                            <p><strong>Status:</strong> {advisor['validity_status']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        status_class = "status-high" if advisor['is_current'] else "status-low"
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>✅ Verification</h4>
                            <div class="status-badge {status_class}">
                                {'VALID' if advisor['is_current'] else 'EXPIRED'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                elif result and result['status'] == 'Not Found':
                    st.error("❌ **Advisor Not Found**")
                    st.info("💡 **Tips:**\n- Check spelling\n- Try partial name search\n- Verify registration number format")
                
                else:
                    st.error("❌ **Verification Failed**")
        
        elif verify_button:
            st.warning("⚠️ Please enter an advisor name or registration number.")
        
        # Sample data display
        with st.expander("📋 Sample Test Data"):
            st.markdown("""
            **Try these sample searches:**
            - **By Name**: John Smith, Priya Sharma, Rajesh Kumar
            - **By RegNo**: IA001234, IA005678, IA009012
            """)
    
    # ===============================
    # TAB 2: FRAUD SCANNER
    # ===============================
    with tab2:
        st.header("🛡️ Fraud Content Scanner")
        st.markdown("Analyze text content for potential financial fraud indicators and get risk assessment.")
        
        # Input methods
        input_method = st.radio(
            "Choose input method:",
            ["📝 Text Analysis", "🔗 URL Analysis"],
            horizontal=True
        )
        
        if input_method == "📝 Text Analysis":
            user_text = st.text_area(
                "📝 Paste content to analyze:",
                placeholder="Example: This investment guarantees 50% returns in just 30 days with no risk involved...",
                height=150,
                help="Paste any suspicious text content"
            )
            
            if st.button("🔍 Analyze Content", type="primary", key="analyze_fraud"):
                if user_text.strip():
                    with st.spinner("Analyzing content for fraud indicators..."):
                        result = analyze_fraud_content(user_text)
                        
                        st.markdown("---")
                        st.subheader("📊 Analysis Results")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("**Original Text:**")
                            st.text_area("", value=user_text, height=100, disabled=True, key="display_text")
                        
                        with col2:
                            risk_level = result["risk_level"]
                            risk_score = result["risk_score"]
                            
                            if risk_level == "High":
                                st.error(f"🔴 **High Risk** (Score: {risk_score})")
                            elif risk_level == "Medium":
                                st.warning(f"🟡 **Medium Risk** (Score: {risk_score})")
                            else:
                                st.success(f"🟢 **Low Risk** (Score: {risk_score})")
                            
                            st.metric("Keywords Detected", len(result["detected_keywords"]))
                        
                        # Detailed analysis
                        if result["detected_keywords"]:
                            st.subheader("🚩 Detected Keywords")
                            
                            for keyword_info in result["detected_keywords"]:
                                risk_emoji = "🔴" if keyword_info["weight"] == 3 else "🟡" if keyword_info["weight"] == 2 else "🟢"
                                st.markdown(f"- {risk_emoji} **{keyword_info['keyword'].title()}** (Risk: {keyword_info['weight']}/3, Count: {keyword_info['count']})")
                            
                            # Recommendations
                            st.subheader("💡 Recommendations")
                            if risk_level == "High":
                                st.error("⚠️ **HIGH RISK**: Do not invest. Report suspicious content.")
                            elif risk_level == "Medium":
                                st.warning("⚠️ **CAUTION**: Verify claims independently.")
                            else:
                                st.info("✅ **LOOKS SAFE**: Still exercise caution with investments.")
                else:
                    st.warning("⚠️ Please enter text to analyze.")
        
        else:  # URL Analysis
            url_input = st.text_input(
                "🔗 Enter URL to analyze:",
                placeholder="https://example.com/investment-opportunity",
                help="Enter web link for analysis"
            )
            
            if st.button("🔍 Analyze Link", type="primary", key="analyze_url"):
                if url_input.strip():
                    st.info("🚧 **URL Analysis**: Feature coming soon. Currently analyzing text content only.")
                else:
                    st.warning("⚠️ Please enter a URL to analyze.")
    
    # ===============================
    # TAB 3: ANNOUNCEMENT VERIFIER
    # ===============================
    with tab3:
        st.header("📊 Corporate Announcement Verifier")
        st.markdown("Fetch and analyze corporate announcements for credibility assessment.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("📈 Latest Announcements")
        
        with col2:
            if st.button("🔄 Fetch Announcements", type="primary"):
                st.session_state.announcements_fetched = True
        
        # Fetch and display announcements
        if st.session_state.get('announcements_fetched', False):
            with st.spinner("Fetching latest announcements..."):
                announcements = fetch_mock_announcements()
                historical_data = load_historical_announcements()
                
                st.success(f"✅ Fetched {len(announcements)} announcements")
                
                # Analyze each announcement
                analyzed_results = []
                for announcement in announcements:
                    credibility, reason, score = analyze_announcement_credibility(
                        announcement["Company"],
                        announcement["AnnouncementText"],
                        historical_data
                    )
                    
                    analyzed_results.append({
                        **announcement,
                        "Credibility": credibility,
                        "Reason": reason,
                        "Score": score
                    })
                
                # Display results
                st.subheader("📋 Analysis Results")
                
                for result in analyzed_results:
                    with st.expander(f"{'🟢' if result['Credibility'] == 'High' else '🟡' if result['Credibility'] == 'Medium' else '🔴'} {result['Company']} - {result['Date']}"):
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("**Announcement:**")
                            st.write(result["AnnouncementText"])
                            
                            st.markdown("**Analysis:**")
                            st.write(result["Reason"])
                        
                        with col2:
                            if result["Credibility"] == "High":
                                st.success(f"✅ **{result['Credibility']} Credibility**")
                            elif result["Credibility"] == "Medium":
                                st.warning(f"⚠️ **{result['Credibility']} Credibility**")
                            else:
                                st.error(f"❌ **{result['Credibility']} Credibility**")
                            
                            st.metric("Credibility Score", f"{result['Score']:.2f}")
        
        else:
            st.info("👆 Click 'Fetch Announcements' to load and analyze corporate announcements.")
        
        # Historical data info
        with st.expander("📚 Historical Data Information"):
            historical_count = len(load_historical_announcements())
            st.info(f"📊 **Historical Database**: {historical_count} records available for comparison analysis.")
    
    # ===============================
    # TAB 4: DEEPFAKE DETECTOR
    # ===============================
    with tab4:
        st.header("🎭 Deepfake Video Detection")
        st.markdown("Upload and analyze video files to detect potential deepfake manipulation.")
        
        # Check API status
        api_status = check_deepfake_api()
        
        if api_status:
            st.success("✅ Deepfake Detection API is online")
            
            # File uploader
            uploaded_file = st.file_uploader(
                "📤 Choose a video file",
                type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
                help="Supported formats: MP4, AVI, MOV, MKV, WEBM. Max size: 50MB"
            )
            
            if uploaded_file is not None:
                # Display file info
                file_size = len(uploaded_file.getvalue())
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**File**: {uploaded_file.name}")
                with col2:
                    st.info(f"**Size**: {file_size / (1024*1024):.1f} MB")
                with col3:
                    st.info(f"**Type**: {uploaded_file.type}")
                
                if file_size > 50 * 1024 * 1024:
                    st.error("❌ File size exceeds 50MB limit.")
                else:
                    if st.button("🔍 Analyze Video", type="primary", key="analyze_deepfake"):
                        with st.spinner("🎯 Analyzing video for deepfake indicators..."):
                            result = analyze_video_deepfake(uploaded_file)
                            
                            if result.get('status') == 'error':
                                st.error(f"❌ **Analysis Failed**: {result.get('error')}")
                            else:
                                st.subheader("📊 Deepfake Analysis Results")
                                
                                fake_probability = float(result.get('fake_probability', 0))
                                risk_level = result.get('risk_level', 'Unknown')
                                
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    if fake_probability < 30:
                                        st.success("✅ **Likely Authentic** - Low manipulation indicators")
                                    elif fake_probability < 70:
                                        st.warning("⚠️ **Uncertain** - Mixed signals detected")
                                    else:
                                        st.error("🚨 **Likely Deepfake** - High manipulation probability")
                                
                                with col2:
                                    st.metric("Fake Probability", f"{fake_probability:.1f}%")
                                    st.metric("Risk Level", risk_level)
            else:
                st.info("👆 Upload a video file to begin deepfake analysis.")
        
        else:
            st.error("❌ Deepfake Detection API is offline")
            st.info("💡 Start the API server: `python deepfake_api.py`")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🛡️ <strong>SEBI Safe Space</strong> - Comprehensive Financial Security Toolkit</p>
        <p>Protect yourself from financial fraud with advanced verification tools</p>
        <p><em>For educational and demonstration purposes only</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()