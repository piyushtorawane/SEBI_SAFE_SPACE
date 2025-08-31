import streamlit as st
import re
from datetime import datetime
from urllib.parse import urlparse

# Fraud detection keywords and their risk levels
FRAUD_KEYWORDS = {
    # High risk keywords
    "guaranteed returns": 3,
    "sure shot tip": 3,
    "ipo allotment guaranteed": 3,
    "doubles your money": 3,
    "inside information": 3,
    "100% guaranteed": 3,
    "risk-free investment": 3,
    "instant profit": 3,
    "insider tips": 3,
    "guaranteed profit": 3,
    "no risk": 3,
    "get rich quick": 3,
    
    # Medium risk keywords
    "hot tip": 2,
    "exclusive opportunity": 2,
    "limited time offer": 2,
    "act now": 2,
    "secret formula": 2,
    "insider knowledge": 2,
    "quick money": 2,
    "easy money": 2,
    "huge returns": 2,
    "minimum investment": 2,
    "once in lifetime": 2,
    "urgent investment": 2,
    
    # Low risk keywords
    "investment opportunity": 1,
    "high returns": 1,
    "profitable": 1,
    "promising stock": 1,
    "good investment": 1,
    "potential gains": 1,
    "market tip": 1,
    "stock recommendation": 1,
}

def is_url(text):
    """Check if the input text is a URL"""
    try:
        result = urlparse(text.strip())
        return all([result.scheme, result.netloc])
    except:
        return False

def analyze_text_for_fraud(text):
    """Analyze text for fraud indicators and calculate risk score"""
    if not text or not isinstance(text, str):
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "detected_keywords": [],
            "total_matches": 0
        }
    
    text_lower = text.lower()
    detected_keywords = []
    total_risk_score = 0
    
    # Check for each fraud keyword
    for keyword, risk_value in FRAUD_KEYWORDS.items():
        if keyword.lower() in text_lower:
            detected_keywords.append({
                "keyword": keyword,
                "risk_value": risk_value,
                "count": text_lower.count(keyword.lower())
            })
            total_risk_score += risk_value * text_lower.count(keyword.lower())
    
    # Calculate risk level based on total score
    if total_risk_score >= 6:
        risk_level = "High"
    elif total_risk_score >= 3:
        risk_level = "Medium"
    elif total_risk_score > 0:
        risk_level = "Low"
    else:
        risk_level = "Low"
    
    return {
        "risk_score": total_risk_score,
        "risk_level": risk_level,
        "detected_keywords": detected_keywords,
        "total_matches": len(detected_keywords)
    }

def get_risk_color(risk_level):
    """Get color coding for risk levels"""
    colors = {
        "Low": "🟢",
        "Medium": "🟡", 
        "High": "🔴"
    }
    return colors.get(risk_level, "⚪")

def display_risk_badge(risk_level):
    """Display colored risk badge"""
    color_map = {
        "Low": "success",
        "Medium": "warning",
        "High": "error"
    }
    
    color = color_map.get(risk_level, "info")
    emoji = get_risk_color(risk_level)
    
    if risk_level == "Low":
        st.success(f"{emoji} **Risk Level: {risk_level}**")
    elif risk_level == "Medium":
        st.warning(f"{emoji} **Risk Level: {risk_level}**")
    else:
        st.error(f"{emoji} **Risk Level: {risk_level}**")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Fraud Content Scanner",
        page_icon="🛡️",
        layout="wide"
    )
    
    # Header
    st.title("🛡️ Fraud Content Scanner")
    st.markdown("---")
    
    # Description
    st.markdown("""
    **Protect yourself from financial fraud!**
    
    This tool analyzes text content and web links to detect potential financial fraud indicators.
    Simply paste your text or enter a URL to get an instant risk assessment.
    """)
    
    # Input section
    st.subheader("📝 Content Analysis")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "URL/Link Input"],
        horizontal=True
    )
    
    if input_method == "Text Input":
        # Text input area
        user_text = st.text_area(
            "Paste the text content you want to analyze:",
            placeholder="Example: This investment guarantees 50% returns in just 30 days with no risk involved...",
            height=150,
            help="Paste any text content like messages, emails, or social media posts"
        )
        
        if st.button("🔍 Analyze Text", type="primary"):
            if user_text.strip():
                with st.spinner("Analyzing content for fraud indicators..."):
                    # Perform fraud analysis
                    analysis_result = analyze_text_for_fraud(user_text)
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")
                    
                    # Create two columns for layout
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**Original Text:**")
                        st.text_area("", value=user_text, height=100, disabled=True)
                    
                    with col2:
                        # Risk level badge
                        display_risk_badge(analysis_result["risk_level"])
                        
                        # Risk score
                        st.metric(
                            label="Risk Score",
                            value=analysis_result["risk_score"],
                            help="Higher scores indicate more suspicious content"
                        )
                        
                        # Detection summary
                        st.metric(
                            label="Suspicious Keywords Found",
                            value=analysis_result["total_matches"]
                        )
                    
                    # Detailed analysis
                    if analysis_result["detected_keywords"]:
                        st.subheader("🚩 Detected Suspicious Keywords")
                        
                        # Create a simple table for better display
                        st.markdown("| Keyword | Risk Level | Occurrences |")
                        st.markdown("|---------|------------|-------------|")
                        
                        for item in analysis_result["detected_keywords"]:
                            risk_emoji = "🔴" if item["risk_value"] == 3 else "🟡" if item["risk_value"] == 2 else "🟢"
                            st.markdown(f"| {item['keyword'].title()} | {risk_emoji} {item['risk_value']}/3 | {item['count']} |")
                        
                        # Recommendations based on risk level
                        st.subheader("💡 Recommendations")
                        if analysis_result["risk_level"] == "High":
                            st.error("""
                            **⚠️ HIGH RISK DETECTED**
                            - This content shows strong indicators of financial fraud
                            - Do NOT invest money based on this information
                            - Report suspicious content to authorities
                            - Verify any investment claims independently
                            """)
                        elif analysis_result["risk_level"] == "Medium":
                            st.warning("""
                            **⚠️ MEDIUM RISK DETECTED**
                            - Exercise extreme caution with this content
                            - Conduct thorough research before making any decisions
                            - Consult with licensed financial advisors
                            - Be skeptical of unrealistic claims
                            """)
                        else:
                            st.info("""
                            **✅ LOW RISK**
                            - Content appears relatively safe, but always exercise caution
                            - Still verify any investment information independently
                            - Consider consulting financial professionals for investment decisions
                            """)
                    else:
                        st.success("✅ No suspicious keywords detected in the content!")
                        st.info("While no obvious fraud indicators were found, always exercise caution with financial decisions.")
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    
    else:  # URL Input
        # URL input
        user_url = st.text_input(
            "Enter the URL/Link you want to analyze:",
            placeholder="https://example.com/suspicious-investment-scheme",
            help="Enter any web link you want to check for potential fraud"
        )
        
        if st.button("🔍 Analyze Link", type="primary"):
            if user_url.strip():
                if is_url(user_url):
                    # Link scanning placeholder
                    st.markdown("---")
                    st.subheader("🔗 Link Analysis")
                    
                    with st.spinner("Scanning link..."):
                        # Simulate processing time
                        import time
                        time.sleep(2)
                    
                    st.info("🚧 **Link scanning placeholder**")
                    st.markdown(f"""
                    **URL:** `{user_url}`
                    
                    **Status:** Link scanning functionality will be expanded in future updates.
                    
                    **Current capabilities:**
                    - Link validation ✅
                    - Basic URL structure analysis ✅
                    - Content extraction (Coming soon)
                    - Domain reputation check (Coming soon)
                    - Website content analysis (Coming soon)
                    """)
                    
                    # Show some basic URL info
                    parsed_url = urlparse(user_url)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**URL Components:**")
                        st.write(f"- **Domain:** {parsed_url.netloc}")
                        st.write(f"- **Scheme:** {parsed_url.scheme}")
                        st.write(f"- **Path:** {parsed_url.path or '/'}")
                    
                    with col2:
                        st.markdown("**Security Tips:**")
                        st.write("- Verify the website domain")
                        st.write("- Check for HTTPS encryption")
                        st.write("- Look for contact information")
                        st.write("- Research the company/service")
                else:
                    st.error("❌ Invalid URL format. Please enter a valid web link starting with http:// or https://")
            else:
                st.warning("⚠️ Please enter a URL to analyze.")
    
    # Footer with information
    st.markdown("---")
    st.subheader("ℹ️ About This Tool")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **How it works:**
        - Scans text for known fraud keywords
        - Calculates risk score based on keyword frequency
        - Provides color-coded risk assessment
        - Offers safety recommendations
        """)
    
    with col2:
        st.markdown("""
        **Fraud Indicators:**
        - 🔴 High risk: Guaranteed returns, insider tips
        - 🟡 Medium risk: Exclusive offers, urgent actions
        - 🟢 Low risk: General investment terms
        """)
    
    # Disclaimer
    with st.expander("⚠️ Important Disclaimer"):
        st.markdown("""
        **Please note:**
        - This tool is for educational and awareness purposes only
        - It does not provide financial advice or investment recommendations
        - Always conduct your own research and consult licensed professionals
        - Report suspected fraud to relevant authorities (SEBI, police, etc.)
        - No tool can guarantee 100% fraud detection
        
        **Emergency Contacts:**
        - SEBI Complaints: complaints@sebi.gov.in
        - Cyber Crime: cybercrime.gov.in
        - Economic Offences Wing: Contact local police
        """)

if __name__ == "__main__":
    main()