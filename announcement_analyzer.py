import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import re
import os
from typing import List, Dict, Tuple
import time
import csv

# Mock BSE API configuration
MOCK_BSE_API_URL = "https://jsonplaceholder.typicode.com/posts"  # Mock API
BSE_COMPANIES = [
    "Reliance Industries", "TCS", "HDFC Bank", "Infosys", "ICICI Bank",
    "Hindustan Unilever", "ITC", "SBI", "Bharti Airtel", "Kotak Mahindra Bank",
    "Larsen & Toubro", "Asian Paints", "Axis Bank", "Maruti Suzuki", "Bajaj Finance"
]

# Credibility analysis keywords
CREDIBILITY_KEYWORDS = {
    "positive_financial": {
        "keywords": ["record profit", "highest revenue", "exceptional growth", "record performance", 
                    "outstanding results", "tremendous growth", "phenomenal success", "breakthrough performance"],
        "weight": 3
    },
    "negative_financial": {
        "keywords": ["massive loss", "significant decline", "worst performance", "financial crisis", 
                    "bankruptcy", "severe losses", "critical situation", "emergency measures"],
        "weight": 3
    },
    "moderate_positive": {
        "keywords": ["good performance", "steady growth", "positive outlook", "improved results", 
                    "satisfactory performance", "progress", "development", "expansion"],
        "weight": 2
    },
    "moderate_negative": {
        "keywords": ["challenging times", "difficult period", "market pressures", "headwinds", 
                    "cautious outlook", "slower growth", "reduced margins", "competitive pressure"],
        "weight": 2
    },
    "neutral": {
        "keywords": ["quarterly results", "board meeting", "dividend declaration", "annual report", 
                    "compliance", "regulatory filing", "announcement", "update"],
        "weight": 1
    }
}

class AnnouncementAnalyzer:
    def __init__(self):
        self.historical_data_file = "historical_announcements.csv"
        self.current_announcements = []
        self.historical_announcements = self.load_historical_data()
    
    def load_historical_data(self) -> List[Dict]:
        """Load historical announcements from CSV file"""
        try:
            if os.path.exists(self.historical_data_file):
                historical_data = []
                with open(self.historical_data_file, 'r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        historical_data.append(row)
                return historical_data
            else:
                # Create mock historical data
                return self.create_mock_historical_data()
        except Exception as e:
            st.error(f"Error loading historical data: {e}")
            return []
    
    def create_mock_historical_data(self) -> List[Dict]:
        """Create mock historical announcements data"""
        mock_data = []
        
        # Past 6 months of mock data
        base_date = datetime.now() - timedelta(days=180)
        
        for i in range(50):  # 50 historical announcements
            company = BSE_COMPANIES[i % len(BSE_COMPANIES)]
            date = base_date + timedelta(days=i*3)
            
            # Create varied announcement types
            if i % 4 == 0:
                announcement = f"{company} reports quarterly loss of ₹{100+i*10} crores due to market challenges"
                sentiment = "negative"
            elif i % 4 == 1:
                announcement = f"{company} announces steady growth with revenue of ₹{500+i*20} crores"
                sentiment = "positive"
            elif i % 4 == 2:
                announcement = f"{company} board meeting scheduled for dividend declaration and corporate governance"
                sentiment = "neutral"
            else:
                announcement = f"{company} faces challenging market conditions with reduced profit margins"
                sentiment = "negative"
            
            mock_data.append({
                "Company": company,
                "Date": date.strftime("%Y-%m-%d"),
                "AnnouncementText": announcement,
                "Sentiment": sentiment
            })
        
        # Save to CSV
        with open(self.historical_data_file, 'w', newline='', encoding='utf-8') as file:
            if mock_data:
                fieldnames = mock_data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(mock_data)
        
        return mock_data
    
    def fetch_latest_announcements(self) -> List[Dict]:
        """Fetch latest announcements from mock BSE API"""
        try:
            # Mock API call - in real scenario, this would be BSE API
            response = requests.get(MOCK_BSE_API_URL, timeout=10)
            
            if response.status_code == 200:
                mock_posts = response.json()[:10]  # Get first 10 posts
                
                announcements = []
                for i, post in enumerate(mock_posts):
                    company = BSE_COMPANIES[i % len(BSE_COMPANIES)]
                    
                    # Create realistic announcement based on post title/body
                    announcement_templates = [
                        f"{company} reports record profit of ₹{1000+i*100} crores in Q{(i%4)+1}",
                        f"{company} announces massive loss of ₹{200+i*50} crores due to market downturn",
                        f"{company} declares exceptional growth with highest revenue in company history",
                        f"{company} faces financial crisis with significant decline in performance",
                        f"{company} board approves dividend and reports steady progress in operations"
                    ]
                    
                    announcement_text = announcement_templates[i % len(announcement_templates)]
                    
                    announcements.append({
                        "Company": company,
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "AnnouncementText": announcement_text,
                        "Source": "BSE India (Mock)"
                    })
                
                return announcements
            else:
                st.error("Failed to fetch announcements from API")
                return []
                
        except Exception as e:
            st.error(f"Error fetching announcements: {e}")
            return self.create_fallback_announcements()
    
    def create_fallback_announcements(self) -> List[Dict]:
        """Create fallback announcements when API is unavailable"""
        fallback_announcements = [
            {
                "Company": "Reliance Industries",
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "AnnouncementText": "Reliance Industries reports record profit of ₹15,000 crores with exceptional growth in digital services",
                "Source": "Mock Data"
            },
            {
                "Company": "TCS",
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "AnnouncementText": "TCS announces massive loss of ₹2,000 crores due to unprecedented market challenges",
                "Source": "Mock Data"
            },
            {
                "Company": "HDFC Bank",
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "AnnouncementText": "HDFC Bank declares highest revenue in banking sector with tremendous growth",
                "Source": "Mock Data"
            }
        ]
        return fallback_announcements
    
    def analyze_announcement_sentiment(self, text: str) -> Tuple[str, int, List[str]]:
        """Analyze announcement text for sentiment and credibility"""
        text_lower = text.lower()
        detected_keywords = []
        total_score = 0
        sentiment_type = "neutral"
        
        for category, data in CREDIBILITY_KEYWORDS.items():
            for keyword in data["keywords"]:
                if keyword.lower() in text_lower:
                    detected_keywords.append({
                        "keyword": keyword,
                        "category": category,
                        "weight": data["weight"]
                    })
                    total_score += data["weight"]
                    
                    # Determine primary sentiment
                    if "positive" in category:
                        sentiment_type = "positive"
                    elif "negative" in category:
                        sentiment_type = "negative"
        
        return sentiment_type, total_score, detected_keywords
    
    def check_credibility_mismatch(self, company: str, current_announcement: str) -> Tuple[str, str, float]:
        """Check for credibility mismatches against historical data"""
        
        # Get historical announcements for this company
        company_history = [item for item in self.historical_announcements if item.get("Company") == company]
        
        if not company_history:
            return "Medium", "No historical data available for comparison", 0.5
        
        # Analyze current announcement
        current_sentiment, current_score, current_keywords = self.analyze_announcement_sentiment(current_announcement)
        
        # Analyze historical sentiment trend
        historical_sentiments = []
        for row in company_history:
            if "Sentiment" in row and row["Sentiment"]:
                historical_sentiments.append(row["Sentiment"])
            else:
                # Analyze historical text if sentiment not available
                hist_sentiment, _, _ = self.analyze_announcement_sentiment(row["AnnouncementText"])
                historical_sentiments.append(hist_sentiment)
        
        # Calculate mismatch
        recent_negative_count = historical_sentiments[-5:].count("negative")  # Last 5 announcements
        recent_positive_count = historical_sentiments[-5:].count("positive")
        
        mismatch_reason = ""
        credibility_score = 0.7  # Default medium credibility
        
        # Check for drastic mismatches
        if current_sentiment == "positive" and recent_negative_count >= 3:
            # Company suddenly reporting positive after multiple negative reports
            if any("record profit" in str(kw.get("keyword", "")) for kw in current_keywords if isinstance(kw, dict)):
                credibility_score = 0.2
                mismatch_reason = f"Claims record profit despite {recent_negative_count} recent negative reports"
            else:
                credibility_score = 0.4
                mismatch_reason = f"Positive announcement conflicts with recent negative trend"
        
        elif current_sentiment == "negative" and recent_positive_count >= 3:
            # Company suddenly reporting negative after positive trend
            if any("massive loss" in str(kw.get("keyword", "")) for kw in current_keywords if isinstance(kw, dict)):
                credibility_score = 0.3
                mismatch_reason = f"Claims massive loss despite recent positive performance"
            else:
                credibility_score = 0.5
                mismatch_reason = f"Negative announcement conflicts with positive trend"
        
        elif current_score >= 6:  # Very strong claims
            credibility_score = 0.4
            mismatch_reason = "Exceptionally strong claims require verification"
        
        else:
            credibility_score = 0.8
            mismatch_reason = "Announcement appears consistent with historical pattern"
        
        # Determine credibility level
        if credibility_score >= 0.7:
            credibility = "High"
        elif credibility_score >= 0.4:
            credibility = "Medium"
        else:
            credibility = "Low"
        
        return credibility, mismatch_reason, credibility_score
    
    def analyze_all_announcements(self, announcements: List[Dict]) -> List[Dict]:
        """Analyze all announcements for credibility"""
        analyzed_data = []
        
        for announcement in announcements:
            company = announcement["Company"]
            text = announcement["AnnouncementText"]
            date = announcement["Date"]
            
            # Perform credibility analysis
            credibility, reason, score = self.check_credibility_mismatch(company, text)
            
            # Get sentiment analysis
            sentiment, sentiment_score, keywords = self.analyze_announcement_sentiment(text)
            
            analyzed_data.append({
                "Company": company,
                "Date": date,
                "AnnouncementText": text,
                "CredibilityLevel": credibility,
                "CredibilityScore": round(score, 2),
                "Reason": reason,
                "Sentiment": sentiment,
                "SentimentScore": sentiment_score,
                "KeywordsDetected": len(keywords),
                "Source": announcement.get("Source", "BSE India")
            })
        
        return analyzed_data

def get_credibility_color(credibility: str) -> str:
    """Get color for credibility level"""
    colors = {
        "High": "🟢",
        "Medium": "🟡",
        "Low": "🔴"
    }
    return colors.get(credibility, "⚪")

def display_credibility_badge(credibility: str):
    """Display colored credibility badge"""
    emoji = get_credibility_color(credibility)
    
    if credibility == "High":
        st.success(f"{emoji} **Credibility: {credibility}**")
    elif credibility == "Medium":
        st.warning(f"{emoji} **Credibility: {credibility}**")
    else:
        st.error(f"{emoji} **Credibility: {credibility}**")

def main():
    # Page configuration
    st.set_page_config(
        page_title="BSE Announcement Analyzer",
        page_icon="📊",
        layout="wide"
    )
    
    # Header
    st.title("📊 BSE Corporate Announcement Analyzer")
    st.markdown("---")
    
    # Description
    st.markdown("""
    **Real-time Corporate Announcement Credibility Analysis**
    
    This dashboard fetches the latest corporate announcements from BSE India and analyzes them for credibility
    by comparing against historical filings and detecting potential mismatches or suspicious claims.
    """)
    
    # Initialize analyzer
    analyzer = AnnouncementAnalyzer()
    
    # Sidebar controls
    st.sidebar.header("🔧 Controls")
    
    if st.sidebar.button("🔄 Fetch Latest Announcements", type="primary"):
        with st.spinner("Fetching latest announcements from BSE..."):
            st.session_state.announcements = analyzer.fetch_latest_announcements()
            st.session_state.analyzed_data = analyzer.analyze_all_announcements(st.session_state.announcements)
        st.sidebar.success("✅ Announcements updated!")
    
    # Auto-fetch on first load
    if 'announcements' not in st.session_state:
        with st.spinner("Loading initial data..."):
            st.session_state.announcements = analyzer.fetch_latest_announcements()
            st.session_state.analyzed_data = analyzer.analyze_all_announcements(st.session_state.announcements)
    
    # Filters
    st.sidebar.subheader("🔍 Filters")
    
    if st.session_state.analyzed_data:
        companies = ["All"] + list(set(item["Company"] for item in st.session_state.analyzed_data))
        selected_company = st.sidebar.selectbox("Company", companies)
        
        credibility_levels = ["All"] + list(set(item["CredibilityLevel"] for item in st.session_state.analyzed_data))
        selected_credibility = st.sidebar.selectbox("Credibility Level", credibility_levels)
        
        # Apply filters
        filtered_data = st.session_state.analyzed_data.copy()
        
        if selected_company != "All":
            filtered_data = [item for item in filtered_data if item["Company"] == selected_company]
        
        if selected_credibility != "All":
            filtered_data = [item for item in filtered_data if item["CredibilityLevel"] == selected_credibility]
    else:
        filtered_data = []
    
    # Main dashboard
    if filtered_data:
        # Summary metrics
        st.subheader("📈 Summary Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_announcements = len(filtered_data)
            st.metric("Total Announcements", total_announcements)
        
        with col2:
            high_credibility = len([item for item in filtered_data if item["CredibilityLevel"] == "High"])
            st.metric("High Credibility", high_credibility, f"{high_credibility/total_announcements*100:.1f}%")
        
        with col3:
            low_credibility = len([item for item in filtered_data if item["CredibilityLevel"] == "Low"])
            st.metric("Low Credibility", low_credibility, f"{low_credibility/total_announcements*100:.1f}%")
        
        with col4:
            avg_score = sum(item["CredibilityScore"] for item in filtered_data) / len(filtered_data)
            st.metric("Avg Credibility Score", f"{avg_score:.2f}")
        
        # Credibility distribution
        st.subheader("🎯 Credibility Distribution")
        credibility_counts = {}
        for item in filtered_data:
            level = item["CredibilityLevel"]
            credibility_counts[level] = credibility_counts.get(level, 0) + 1
        
        if credibility_counts:
            st.bar_chart(credibility_counts)
        
        # Detailed announcements
        st.subheader("📋 Detailed Analysis")
        
        for item in filtered_data:
            with st.expander(f"{get_credibility_color(item['CredibilityLevel'])} {item['Company']} - {item['Date']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Announcement:**")
                    st.write(item["AnnouncementText"])
                    
                    st.markdown("**Analysis Reason:**")
                    st.write(item["Reason"])
                
                with col2:
                    display_credibility_badge(item["CredibilityLevel"])
                    
                    st.metric("Credibility Score", f"{item['CredibilityScore']:.2f}")
                    st.metric("Sentiment Score", item["SentimentScore"])
                    st.metric("Keywords Detected", item["KeywordsDetected"])
                    
                    # Sentiment indicator
                    if item["Sentiment"] == "positive":
                        st.success(f"📈 {item['Sentiment'].title()}")
                    elif item["Sentiment"] == "negative":
                        st.error(f"📉 {item['Sentiment'].title()}")
                    else:
                        st.info(f"📊 {item['Sentiment'].title()}")
        
        # Data table
        st.subheader("📊 Raw Data")
        
        # Convert to display format
        display_data = []
        for item in filtered_data:
            display_data.append({
                "Company": item["Company"],
                "Date": item["Date"],
                "CredibilityLevel": item["CredibilityLevel"],
                "CredibilityScore": item["CredibilityScore"],
                "Sentiment": item["Sentiment"],
                "Reason": item["Reason"]
            })
        
        st.dataframe(display_data, use_container_width=True)
        
        # Download option
        csv_content = "Company,Date,CredibilityLevel,CredibilityScore,Sentiment,Reason\n"
        for item in filtered_data:
            csv_content += f"{item['Company']},{item['Date']},{item['CredibilityLevel']},{item['CredibilityScore']},{item['Sentiment']},\"{item['Reason']}\"\n"
        
        st.download_button(
            label="📥 Download Analysis as CSV",
            data=csv_content,
            file_name=f"bse_announcements_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    else:
        st.info("No announcements available. Click 'Fetch Latest Announcements' to load data.")
    
    # Historical data section
    st.markdown("---")
    st.subheader("📚 Historical Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Historical Announcements Database:**")
        if analyzer.historical_announcements:
            st.success(f"✅ {len(analyzer.historical_announcements)} historical records loaded")
            
            with st.expander("View Historical Data Sample"):
                # Show first 10 records
                sample_data = analyzer.historical_announcements[:10]
                for i, record in enumerate(sample_data):
                    st.write(f"{i+1}. {record['Company']} ({record['Date']}): {record['AnnouncementText'][:60]}...")
        else:
            st.warning("⚠️ No historical data available")
    
    with col2:
        st.markdown("**Analysis Methodology:**")
        st.markdown("""
        - **High Credibility**: Consistent with historical pattern
        - **Medium Credibility**: Some concerns or limited data
        - **Low Credibility**: Contradicts recent filings or extreme claims
        
        **Red Flags:**
        - Record profits after recent losses
        - Massive losses after positive trend
        - Exceptionally strong claims
        """)
    
    # Footer
    st.markdown("---")
    with st.expander("ℹ️ About This System"):
        st.markdown("""
        **Technical Implementation:**
        - **Data Source**: BSE India API (Mock implementation)
        - **Analysis Engine**: Historical pattern matching and sentiment analysis
        - **Credibility Scoring**: Multi-factor analysis including keyword detection and trend comparison
        
        **Disclaimer:**
        - This tool is for research and educational purposes only
        - Not intended as investment advice
        - Always verify information from official sources
        - Consult financial professionals for investment decisions
        
        **Data Sources:**
        - Mock BSE API for demonstration
        - Historical announcement patterns
        - Keyword-based sentiment analysis
        """)

if __name__ == "__main__":
    main()