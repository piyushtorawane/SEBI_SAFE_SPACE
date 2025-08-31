import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"
VERIFY_ENDPOINT = f"{API_BASE_URL}/verify_advisor"

def call_verify_api(query):
    """Call the Flask API to verify advisor"""
    try:
        payload = {"query": query}
        response = requests.post(VERIFY_ENDPOINT, json=payload, timeout=10)
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return None, {"error": "Cannot connect to API. Make sure Flask server is running on localhost:5000"}
    except requests.exceptions.Timeout:
        return None, {"error": "Request timed out"}
    except Exception as e:
        return None, {"error": f"Unexpected error: {str(e)}"}

def display_advisor_details(advisor_details):
    """Display advisor details in a formatted way"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Name:**", advisor_details['name'])
        st.write("**Registration Number:**", advisor_details['registration_number'])
    
    with col2:
        st.write("**Validity Date:**", advisor_details['validity'])
        
        # Display validity status with color coding
        if advisor_details['is_current']:
            st.success(f"✅ {advisor_details['validity_status']}")
        else:
            st.error(f"❌ {advisor_details['validity_status']}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="SEBI Advisor Verification",
        page_icon="🔍",
        layout="wide"
    )
    
    # Header
    st.title("🔍 SEBI Advisor Verification System")
    st.markdown("---")
    
    # Description
    st.markdown("""
    **Welcome to the SEBI Advisor Verification System!**
    
    This tool allows you to verify if an investment advisor is registered with SEBI (Securities and Exchange Board of India).
    You can search by:
    - Advisor Name (partial matches supported)
    - Registration Number (exact match)
    """)
    
    # Input section
    st.subheader("🔎 Search for an Advisor")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter Advisor Name or Registration Number:",
            placeholder="e.g., John Smith or IA001234",
            help="You can enter a partial name or exact registration number"
        )
    
    with col2:
        st.write("")  # Add some spacing
        search_button = st.button("🔍 Verify", type="primary")
    
    # Search logic
    if search_button or (query and len(query.strip()) > 0):
        if not query.strip():
            st.warning("⚠️ Please enter an advisor name or registration number to search.")
            return
        
        # Show loading spinner
        with st.spinner("Verifying advisor..."):
            status_code, response = call_verify_api(query.strip())
        
        # Handle API connection errors
        if status_code is None:
            st.error(f"🚫 **Connection Error:** {response['error']}")
            st.info("💡 **Tip:** Make sure the Flask API server is running. Run `python app.py` in your terminal.")
            return
        
        # Handle API responses
        if status_code == 200:
            if response['status'] == 'Verified':
                st.success("✅ **Advisor Found and Verified!**")
                
                # Display advisor details in an expandable container
                with st.container():
                    st.subheader("📋 Advisor Details")
                    display_advisor_details(response['advisor_details'])
                    
                    # Additional info
                    st.info("ℹ️ This advisor is registered with SEBI.")
                    
            elif response['status'] == 'Not Found':
                st.error("❌ **Advisor Not Found**")
                st.write(response.get('message', 'The advisor was not found in the SEBI database.'))
                st.info("💡 **Tips:**\n- Check the spelling of the advisor's name\n- Verify the registration number\n- Try searching with partial name")
        
        elif status_code == 400:
            st.error("🚫 **Invalid Request**")
            st.write(response.get('message', 'Please check your input and try again.'))
        
        elif status_code == 500:
            st.error("🚫 **Server Error**")
            st.write(response.get('message', 'Internal server error occurred.'))
        
        else:
            st.error(f"🚫 **Unexpected Error** (Status: {status_code})")
            st.write(response.get('message', 'An unexpected error occurred.'))
    
    # Footer section
    st.markdown("---")
    st.subheader("ℹ️ How to Use")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Search by Name:**
        - Enter full or partial advisor name
        - Search is case-insensitive
        - Example: "John" will find "John Smith"
        """)
    
    with col2:
        st.markdown("""
        **Search by Registration Number:**
        - Enter exact registration number
        - Format: IA followed by numbers
        - Example: "IA001234"
        """)
    
    # Status indicator
    st.markdown("---")
    st.subheader("🌐 System Status")
    
    # Quick health check
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API Server is running")
        else:
            st.error("❌ API Server is not responding correctly")
    except:
        st.error("❌ API Server is not accessible")
        st.info("Make sure to run `python app.py` to start the Flask server")

    # Sample data info
    with st.expander("📊 Sample Data Information"):
        st.markdown("""
        **Available Test Advisors:**
        - John Smith (IA001234)
        - Priya Sharma (IA005678)
        - Rajesh Kumar (IA009012)
        - Anita Desai (IA003456)
        - And more...
        
        You can search for any of these names or registration numbers to test the system.
        """)

if __name__ == "__main__":
    main()