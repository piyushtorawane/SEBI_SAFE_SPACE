import streamlit as st
import requests
import os
import tempfile
from datetime import datetime
import json
import time

# Configuration
DEEPFAKE_API_URL = "http://localhost:5001"
ANALYZE_ENDPOINT = f"{DEEPFAKE_API_URL}/analyze_video"
HEALTH_ENDPOINT = f"{DEEPFAKE_API_URL}/health"

def check_api_status():
    """Check if the deepfake detection API is running"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_video_file(video_file):
    """Send video file to API for analysis"""
    try:
        # Prepare file for upload
        files = {'video': (video_file.name, video_file.getvalue(), 'video/mp4')}
        
        # Make API request
        response = requests.post(ANALYZE_ENDPOINT, files=files, timeout=120)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return {
                'error': error_data.get('error', f'API Error: {response.status_code}'),
                'status': 'error'
            }
            
    except requests.exceptions.Timeout:
        return {'error': 'Request timeout - video analysis took too long', 'status': 'error'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Cannot connect to deepfake detection API', 'status': 'error'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}', 'status': 'error'}

def get_risk_color(risk_level):
    """Get color emoji for risk level"""
    colors = {
        "Low": "🟢",
        "Medium": "🟡", 
        "High": "🔴"
    }
    return colors.get(risk_level, "⚪")

def display_risk_badge(risk_level, fake_probability):
    """Display colored risk badge"""
    emoji = get_risk_color(risk_level)
    
    if risk_level == "Low":
        st.success(f"{emoji} **{risk_level} Risk** ({fake_probability}% fake probability)")
    elif risk_level == "Medium":
        st.warning(f"{emoji} **{risk_level} Risk** ({fake_probability}% fake probability)")
    else:
        st.error(f"{emoji} **{risk_level} Risk** ({fake_probability}% fake probability)")

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def display_detailed_analysis(analysis_data):
    """Display detailed analysis results"""
    if 'detailed_analysis' not in analysis_data:
        return
    
    detailed = analysis_data['detailed_analysis']
    
    st.subheader("🔍 Detailed Analysis")
    
    # Create tabs for different analysis types
    tab1, tab2, tab3 = st.tabs(["👤 Face Analysis", "⏱️ Temporal Analysis", "🤖 AI Analysis"])
    
    with tab1:
        face_analysis = detailed.get('face_consistency', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Faces Detected", f"{face_analysis.get('avg_face_count', 0):.1f}")
            st.metric("Face Count Variance", f"{face_analysis.get('face_count_variance', 0):.2f}")
        
        with col2:
            st.metric("Average Face Size", f"{face_analysis.get('avg_face_size', 0):.0f} pixels")
            st.metric("Consistency Score", f"{face_analysis.get('consistency_score', 0):.2f}")
        
        # Consistency explanation
        consistency_score = face_analysis.get('consistency_score', 0)
        if consistency_score > 0.8:
            st.success("✅ High facial consistency across frames")
        elif consistency_score > 0.5:
            st.warning("⚠️ Moderate facial consistency")
        else:
            st.error("❌ Low facial consistency - potential manipulation detected")
    
    with tab2:
        temporal_analysis = detailed.get('temporal_analysis', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Temporal Score", f"{temporal_analysis.get('temporal_score', 0):.2f}")
            st.metric("Frame Difference Mean", f"{temporal_analysis.get('diff_mean', 0):.2f}")
        
        with col2:
            st.metric("Frame Difference Variance", f"{temporal_analysis.get('diff_variance', 0):.2f}")
        
        # Temporal explanation
        temporal_score = temporal_analysis.get('temporal_score', 0)
        if temporal_score > 0.7:
            st.success("✅ Natural temporal progression")
        elif temporal_score > 0.4:
            st.warning("⚠️ Some temporal irregularities")
        else:
            st.error("❌ Irregular temporal patterns detected")
    
    with tab3:
        ai_analysis = detailed.get('ai_analysis', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("AI Fake Probability", f"{ai_analysis.get('ai_fake_probability', 0):.1f}%")
            st.metric("Model Confidence", f"{ai_analysis.get('confidence', 0):.2f}")
        
        with col2:
            st.info(f"**Model**: {ai_analysis.get('model_version', 'Unknown')}")
        
        # AI explanation
        ai_prob = ai_analysis.get('ai_fake_probability', 0)
        if ai_prob < 30:
            st.success("✅ AI model indicates likely authentic")
        elif ai_prob < 70:
            st.warning("⚠️ AI model shows mixed signals")
        else:
            st.error("❌ AI model indicates likely deepfake")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Deepfake Detection",
        page_icon="🎭",
        layout="wide"
    )
    
    # Header
    st.title("🎭 Deepfake Video Detection")
    st.markdown("---")
    
    # Description
    st.markdown("""
    **AI-Powered Video Authenticity Analysis**
    
    Upload a video file to analyze if it has been manipulated using deepfake technology.
    Our system uses multiple detection methods including facial consistency analysis,
    temporal pattern recognition, and AI-based classification.
    """)
    
    # API Status Check
    api_status = check_api_status()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if api_status:
            st.success("✅ Deepfake Detection API is online")
        else:
            st.error("❌ Deepfake Detection API is offline")
            st.info("Please start the API server by running: `python deepfake_api.py`")
    
    with col2:
        if st.button("🔄 Check API Status"):
            st.rerun()
    
    # Main interface
    if not api_status:
        st.stop()
    
    st.markdown("---")
    st.subheader("📤 Upload Video for Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a video file",
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
            st.info(f"**Size**: {format_file_size(file_size)}")
        with col3:
            st.info(f"**Type**: {uploaded_file.type}")
        
        # Check file size
        if file_size > 50 * 1024 * 1024:  # 50MB
            st.error("❌ File size exceeds 50MB limit. Please upload a smaller file.")
            return
        
        # Analysis button
        if st.button("🔍 Analyze Video", type="primary"):
            
            with st.spinner("🎯 Analyzing video for deepfake indicators..."):
                # Add progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress updates
                for i in range(1, 4):
                    status_text.text(f"Step {i}/3: {'Uploading file...' if i==1 else 'Extracting frames...' if i==2 else 'Running AI analysis...'}")
                    progress_bar.progress(i * 30)
                    time.sleep(1)
                
                # Perform actual analysis
                result = analyze_video_file(uploaded_file)
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                
                # Clear progress indicators
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            if result.get('status') == 'error':
                st.error(f"❌ **Analysis Failed**: {result.get('error')}")
                
                # Troubleshooting tips
                with st.expander("🛠️ Troubleshooting Tips"):
                    st.markdown("""
                    **Common Issues:**
                    - **API Connection**: Ensure the deepfake API is running on port 5001
                    - **File Format**: Only MP4, AVI, MOV, MKV, WEBM are supported
                    - **File Size**: Maximum 50MB file size limit
                    - **Video Quality**: Very short or corrupted videos may fail analysis
                    
                    **Solutions:**
                    1. Check API status above
                    2. Try a different video file
                    3. Ensure video is not corrupted
                    4. Restart the API server if needed
                    """)
            else:
                # Success - display results
                fake_probability = float(result.get('fake_probability', 0))
                risk_level = result.get('risk_level', 'Unknown')
                confidence = float(result.get('confidence', 0))
                
                # Main result display
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    display_risk_badge(risk_level, fake_probability)
                    
                    # Interpretation
                    if fake_probability < 30:
                        st.success("""
                        ✅ **Likely Authentic**
                        The video shows strong indicators of being genuine with minimal signs of manipulation.
                        """)
                    elif fake_probability < 70:
                        st.warning("""
                        ⚠️ **Uncertain/Mixed Signals**
                        The analysis shows some potential indicators of manipulation. Further verification recommended.
                        """)
                    else:
                        st.error("""
                        🚨 **Likely Deepfake**
                        Strong indicators suggest this video may be artificially generated or heavily manipulated.
                        """)
                
                with col2:
                    st.metric("Fake Probability", f"{fake_probability:.1f}%")
                    st.metric("Model Confidence", f"{confidence:.1f}")
                    st.metric("Frames Analyzed", result.get('frames_analyzed', 'N/A'))
                
                # Video information
                if 'video_info' in result and isinstance(result['video_info'], dict):
                    st.subheader("📹 Video Information")
                    
                    video_info = result['video_info']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Duration", f"{video_info.get('duration', 0):.1f}s")
                    with col2:
                        st.metric("FPS", f"{video_info.get('fps', 0):.1f}")
                    with col3:
                        st.metric("Resolution", video_info.get('resolution', 'Unknown'))
                    with col4:
                        st.metric("Total Frames", video_info.get('frame_count', 0))
                
                # Detailed analysis
                display_detailed_analysis(result)
                
                # Analysis metadata
                with st.expander("ℹ️ Analysis Metadata"):
                    st.json({
                        'filename': result.get('filename'),
                        'analysis_timestamp': result.get('analysis_timestamp'),
                        'upload_timestamp': result.get('upload_timestamp')
                    })
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Detection Methods:**
        - **Facial Consistency**: Analyzes facial landmarks and proportions
        - **Temporal Analysis**: Examines frame-to-frame transitions
        - **AI Classification**: Machine learning-based detection
        - **Metadata Analysis**: Video encoding and compression patterns
        """)
    
    with col2:
        st.markdown("""
        **Risk Levels:**
        - 🟢 **Low (0-30%)**: Likely authentic video
        - 🟡 **Medium (30-70%)**: Uncertain, needs verification
        - 🔴 **High (70-100%)**: Likely deepfake or manipulated
        """)
    
    # Disclaimer and limitations
    with st.expander("⚠️ Important Disclaimer"):
        st.markdown("""
        **Limitations & Important Notes:**
        
        - This tool is for educational and research purposes only
        - No deepfake detection system is 100% accurate
        - Results should be used as guidance, not definitive proof
        - Always verify important content through multiple sources
        - False positives and negatives are possible
        - The tool works best with clear, high-quality videos
        
        **Legal Notice:**
        - Do not use for malicious purposes
        - Respect privacy and consent when analyzing videos
        - This tool does not constitute legal evidence
        - Always comply with local laws and regulations
        
        **Technical Limitations:**
        - Analysis quality depends on video quality
        - Very short videos may have limited accuracy
        - Compressed or low-resolution videos may affect results
        - The system may not detect all types of manipulation
        """)

if __name__ == "__main__":
    main()