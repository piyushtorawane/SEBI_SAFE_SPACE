# Deepfake Video Detection System

A comprehensive Python application that analyzes video files to detect potential deepfake or manipulated content using computer vision techniques and AI analysis.

## Features

### 🎭 **Advanced Detection Methods**
- **Facial Consistency Analysis**: Detects inconsistencies in facial landmarks and proportions
- **Temporal Pattern Analysis**: Examines frame-to-frame transitions for unnatural patterns
- **AI-Based Classification**: Simulated deep learning model for deepfake detection
- **Metadata Analysis**: Video encoding and compression pattern examination

### 🔍 **Multi-Factor Analysis**
- **Face Detection**: OpenCV-based facial recognition across video frames
- **Consistency Scoring**: Statistical analysis of facial features over time
- **Temporal Smoothness**: Detection of irregular frame transitions
- **Risk Assessment**: Combined scoring from multiple detection methods

### 📊 **Interactive Dashboard**
- **Streamlit Frontend**: User-friendly web interface for video upload
- **Real-time Analysis**: Live progress tracking during video processing
- **Color-coded Results**: Visual risk indicators (🟢 Low, 🟡 Medium, 🔴 High)
- **Detailed Reports**: Comprehensive analysis breakdown with explanations

### 🔧 **Robust API**
- **Flask Backend**: RESTful API for video analysis
- **File Upload Handling**: Secure file processing with validation
- **Error Management**: Comprehensive error handling and user feedback
- **Health Monitoring**: API status and performance tracking

## Technical Architecture

### Backend Components
- **Flask API Server**: Handles video upload and analysis requests
- **OpenCV Processing**: Frame extraction and facial detection
- **Analysis Engine**: Multi-method deepfake detection algorithms
- **File Management**: Secure upload handling with cleanup

### Frontend Components  
- **Streamlit Interface**: Interactive web application
- **File Upload Widget**: Drag-and-drop video upload
- **Progress Tracking**: Real-time analysis status updates
- **Results Visualization**: Detailed analysis display with charts

### Analysis Pipeline
1. **Video Upload**: Secure file upload with format validation
2. **Frame Extraction**: Extract representative frames from video
3. **Face Detection**: Identify and analyze faces in each frame
4. **Consistency Analysis**: Calculate facial consistency scores
5. **Temporal Analysis**: Examine frame-to-frame transitions
6. **AI Simulation**: Mock deep learning analysis
7. **Risk Calculation**: Combine all scores for final assessment

## Installation & Setup

### Prerequisites
- Python 3.9+
- OpenCV (computer vision library)
- Flask (web framework)
- Streamlit (frontend framework)
- NumPy (numerical computations)

### Quick Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install flask flask-cors streamlit opencv-python numpy werkzeug
```

### Directory Structure
```
SEBI hack/
├── deepfake_api.py              # Flask backend API
├── deepfake_detector.py         # Streamlit frontend
├── test_deepfake_detector.py    # Test suite
├── uploads/                     # Temporary upload directory
└── requirements.txt             # Dependencies
```

## Usage Guide

### 1. **Start the Backend API**
```bash
python deepfake_api.py
```
- API runs on `http://localhost:5001`
- Handles video upload and analysis
- Provides RESTful endpoints

### 2. **Launch the Frontend**
```bash
streamlit run deepfake_detector.py --server.port 8504
```
- Web interface available at `http://localhost:8504`
- User-friendly video upload and analysis
- Real-time results display

### 3. **Using the Interface**
1. **Upload Video**: Drag and drop or select video file
2. **File Validation**: System checks format and size
3. **Analysis**: Click "Analyze Video" to start processing
4. **Results**: View detailed analysis with risk assessment

## Supported Formats

### Video Types
- **MP4** (.mp4) - Most common format
- **AVI** (.avi) - Older standard format
- **MOV** (.mov) - Apple QuickTime format
- **MKV** (.mkv) - Matroska container
- **WEBM** (.webm) - Web-optimized format

### File Limitations
- **Maximum Size**: 50MB per file
- **Minimum Duration**: 1 second recommended
- **Resolution**: Any resolution supported
- **Frame Rate**: Any frame rate supported

## Analysis Methods

### 1. **Facial Consistency Analysis**
**Purpose**: Detect inconsistencies in facial features across frames

**Process**:
- Extract faces from video frames using OpenCV
- Calculate face count, size, and position statistics
- Measure variance in facial characteristics
- Generate consistency score (0.0-1.0)

**Indicators**:
- High variance in face count = potential manipulation
- Irregular face sizes = possible face swapping
- Inconsistent positions = deepfake artifacts

### 2. **Temporal Pattern Analysis**
**Purpose**: Examine frame-to-frame transitions for unnatural patterns

**Process**:
- Calculate pixel differences between consecutive frames
- Analyze temporal smoothness and consistency
- Detect irregular transition patterns
- Generate temporal score (0.0-1.0)

**Indicators**:
- Sudden frame changes = potential editing
- Irregular motion patterns = synthetic generation
- Unnatural temporal flow = deepfake processing

### 3. **AI-Based Classification**
**Purpose**: Simulate advanced deep learning detection

**Process**:
- Mock neural network analysis (simulated)
- Consider video characteristics and metadata
- Apply probabilistic assessment algorithms
- Generate AI confidence score

**Features**:
- Simulates state-of-the-art detection models
- Provides confidence metrics
- Considers multiple detection factors

## Risk Assessment

### Risk Levels

#### 🟢 **Low Risk (0-30%)**
- **Interpretation**: Video appears authentic
- **Characteristics**: Consistent facial features, natural transitions
- **Recommendation**: Likely genuine content

#### 🟡 **Medium Risk (30-70%)**
- **Interpretation**: Mixed signals detected
- **Characteristics**: Some inconsistencies, requires verification
- **Recommendation**: Further analysis recommended

#### 🔴 **High Risk (70-100%)**
- **Interpretation**: Strong deepfake indicators
- **Characteristics**: Multiple manipulation indicators detected
- **Recommendation**: Likely synthetic or heavily edited

### Scoring Formula
```
Final Score = (Consistency_Score × 0.3) + 
              (Temporal_Score × 0.3) + 
              (AI_Score × 0.4)
```

## API Reference

### Endpoints

#### `POST /analyze_video`
**Purpose**: Upload and analyze video for deepfake detection

**Request**:
```bash
curl -X POST http://localhost:5001/analyze_video \
  -F "video=@sample_video.mp4"
```

**Response**:
```json
{
  "fake_probability": 25.7,
  "risk_level": "Low",
  "confidence": 0.85,
  "video_info": {
    "duration": 10.5,
    "fps": 30.0,
    "resolution": "1920x1080",
    "frame_count": 315
  },
  "detailed_analysis": {
    "face_consistency": {
      "consistency_score": 0.82
    },
    "temporal_analysis": {
      "temporal_score": 0.78
    },
    "ai_analysis": {
      "ai_fake_probability": 22.1,
      "confidence": 0.85
    }
  }
}
```

#### `GET /health`
**Purpose**: Check API status and health

**Response**:
```json
{
  "status": "healthy",
  "service": "Deepfake Detection API",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /`
**Purpose**: Get API information and capabilities

**Response**:
```json
{
  "message": "Deepfake Detection API",
  "version": "1.0.0",
  "supported_formats": ["mp4", "avi", "mov", "mkv", "webm"],
  "max_file_size": "50MB"
}
```

## Testing

### Automated Test Suite
```bash
python test_deepfake_detector.py
```

**Test Coverage**:
- ✅ API connectivity and health
- ✅ File upload validation
- ✅ Error handling (no file, invalid format)
- ✅ Mock video analysis
- ✅ Streamlit integration
- ✅ Response format validation

### Manual Testing
1. **Start API**: `python deepfake_api.py`
2. **Test Health**: Visit `http://localhost:5001/health`
3. **Upload Test**: Use test page at `http://localhost:5001/upload_test`
4. **Frontend Test**: Launch Streamlit and upload sample video

## Configuration

### API Settings
```python
# deepfake_api.py configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
```

### Analysis Parameters
```python
# Frame extraction settings
MAX_FRAMES = 30  # Maximum frames to analyze
FRAME_SKIP = "auto"  # Auto-calculate frame skip

# Detection thresholds
CONSISTENCY_THRESHOLD = 0.7
TEMPORAL_THRESHOLD = 0.6
AI_CONFIDENCE_THRESHOLD = 0.8
```

## Performance Optimization

### Processing Efficiency
- **Frame Sampling**: Analyzes representative frames, not all frames
- **Parallel Processing**: Multiple analysis methods run concurrently
- **Memory Management**: Efficient video loading and cleanup
- **Caching**: Results cached for repeated analysis

### Scalability Considerations
- **File Size Limits**: 50MB maximum to prevent resource exhaustion
- **Timeout Settings**: 120-second analysis timeout
- **Cleanup Procedures**: Automatic file deletion after analysis
- **Error Recovery**: Graceful handling of processing failures

## Security & Privacy

### File Handling Security
- **Secure Filenames**: Uses `secure_filename()` for safe file handling
- **Temporary Storage**: Files deleted immediately after analysis
- **Upload Validation**: Strict file type and size validation
- **Path Protection**: No directory traversal vulnerabilities

### Privacy Protection
- **No Permanent Storage**: Videos not stored permanently
- **Local Processing**: All analysis done locally, no external APIs
- **No Data Logging**: Video content not logged or transmitted
- **Clean Deletion**: Secure file cleanup after processing

## Troubleshooting

### Common Issues

#### API Connection Problems
**Symptoms**: "Cannot connect to API" error
**Solutions**:
- Ensure API is running: `python deepfake_api.py`
- Check port 5001 is available
- Verify firewall settings

#### File Upload Failures
**Symptoms**: "File type not supported" or upload errors
**Solutions**:
- Check file format (MP4, AVI, MOV, MKV, WEBM only)
- Verify file size under 50MB
- Ensure file is not corrupted

#### Analysis Errors
**Symptoms**: "Could not extract frames" or processing failures
**Solutions**:
- Try different video file
- Check video codec compatibility
- Ensure OpenCV is properly installed

#### Performance Issues
**Symptoms**: Slow analysis or timeouts
**Solutions**:
- Use shorter video clips
- Reduce video resolution
- Close other applications to free memory

### Error Codes
- **400**: Bad request (invalid file, missing parameters)
- **413**: File too large (exceeds 50MB limit)
- **415**: Unsupported media type
- **500**: Internal server error (processing failure)

## Future Enhancements

### Planned Features
1. **Real AI Integration**: Replace mock AI with actual deepfake detection models
2. **Batch Processing**: Analyze multiple videos simultaneously
3. **Advanced Metrics**: More sophisticated detection algorithms
4. **Result History**: Store and track analysis results
5. **User Authentication**: Secure access and user management

### Integration Possibilities
- **DeepFace Library**: Advanced facial analysis capabilities
- **Hive AI API**: Cloud-based deepfake detection service
- **Custom ML Models**: Train domain-specific detection models
- **Video Forensics**: Integration with digital forensics tools

## Legal & Ethical Considerations

### Responsible Use
- **Educational Purpose**: Tool designed for research and education
- **Consent Required**: Only analyze videos with proper authorization
- **No Malicious Use**: Do not use for harassment or false accusations
- **Legal Compliance**: Follow local laws and regulations

### Limitations
- **Not 100% Accurate**: No detection system is perfect
- **False Positives**: Legitimate videos may be flagged
- **False Negatives**: Some deepfakes may not be detected
- **Evidence Quality**: Results are investigative, not legal proof

### Disclaimer
This tool is provided for educational and research purposes only. Results should not be considered definitive proof of manipulation. Always verify important content through multiple sources and expert analysis.

## Support & Documentation

### Getting Help
- **Test Suite**: Run `python test_deepfake_detector.py` for diagnostics
- **API Documentation**: Visit `http://localhost:5001/` for API info
- **Log Files**: Check console output for detailed error messages
- **Dependencies**: Ensure all packages in `requirements.txt` are installed

### Version Information
- **Current Version**: 1.0.0
- **Python Compatibility**: 3.9+
- **Framework Versions**: Flask 2.3.3, Streamlit 1.28.1, OpenCV 4.8.1

## License

This deepfake detection system is part of the SEBI Financial Security Toolkit and is provided for educational and demonstration purposes.