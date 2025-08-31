from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
import shutil
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

class DeepfakeDetector:
    """
    Deepfake detection using multiple approaches:
    1. Frame extraction and analysis
    2. Facial landmark inconsistency detection
    3. Temporal analysis
    4. Mock AI model simulation
    """
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.analysis_results = {}
    
    def extract_frames(self, video_path, max_frames=30):
        """Extract frames from video for analysis"""
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Calculate frame skip to get evenly distributed frames
            skip = max(1, frame_count // max_frames)
            
            frame_num = 0
            while cap.isOpened() and len(frames) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_num % skip == 0:
                    frames.append(frame)
                
                frame_num += 1
            
            cap.release()
            
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames, fps, frame_count
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return [], 0, 0
    
    def detect_faces_in_frame(self, frame):
        """Detect faces in a single frame"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            return faces
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
    
    def analyze_face_consistency(self, frames):
        """Analyze facial consistency across frames"""
        try:
            face_counts = []
            face_sizes = []
            face_positions = []
            
            for frame in frames:
                faces = self.detect_faces_in_frame(frame)
                face_counts.append(len(faces))
                
                for (x, y, w, h) in faces:
                    face_sizes.append(w * h)
                    face_positions.append((x + w//2, y + h//2))
            
            # Calculate consistency metrics
            avg_face_count = np.mean(face_counts) if face_counts else 0
            face_count_variance = np.var(face_counts) if face_counts else 0
            
            avg_face_size = np.mean(face_sizes) if face_sizes else 0
            face_size_variance = np.var(face_sizes) if face_sizes else 0
            
            # Higher variance indicates potential manipulation
            consistency_score = 1.0 - min(1.0, float(face_count_variance + face_size_variance / 10000) / 10)
            
            return {
                'avg_face_count': avg_face_count,
                'face_count_variance': face_count_variance,
                'avg_face_size': avg_face_size,
                'face_size_variance': face_size_variance,
                'consistency_score': consistency_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing face consistency: {e}")
            return {'consistency_score': 0.5}
    
    def analyze_temporal_features(self, frames):
        """Analyze temporal features for deepfake detection"""
        try:
            if len(frames) < 3:
                return {'temporal_score': 0.5}
            
            # Calculate frame differences
            frame_diffs = []
            for i in range(len(frames) - 1):
                diff = cv2.absdiff(frames[i], frames[i + 1])
                frame_diffs.append(np.mean(diff))
            
            # Calculate temporal consistency
            diff_variance = np.var(frame_diffs)
            diff_mean = np.mean(frame_diffs)
            
            # Normalize temporal score (lower variance = more consistent = less likely to be fake)
            temporal_score = max(0.0, min(1.0, 1.0 - float(diff_variance) / (float(diff_mean) + 1)))
            
            return {
                'frame_differences': frame_diffs,
                'diff_variance': diff_variance,
                'diff_mean': diff_mean,
                'temporal_score': temporal_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing temporal features: {e}")
            return {'temporal_score': 0.5}
    
    def mock_ai_analysis(self, video_info):
        """Mock AI-based deepfake detection simulation"""
        try:
            # Simulate advanced AI model analysis
            # In real implementation, this would call actual AI models
            
            # Base fake probability on various factors
            base_probability = 15.0  # Base 15% chance
            
            # Adjust based on video characteristics
            duration_factor = min(10.0, video_info.get('duration', 5) / 10)  # Longer videos slightly more suspicious
            frame_count_factor = min(5.0, video_info.get('frame_count', 100) / 1000)  # More frames = more data
            
            # Add some randomness to simulate AI uncertainty
            import random
            random_factor = random.uniform(-10, 15)
            
            mock_probability = base_probability + duration_factor + frame_count_factor + random_factor
            mock_probability = max(0.0, min(100.0, mock_probability))
            
            return {
                'ai_fake_probability': mock_probability,
                'confidence': random.uniform(0.7, 0.95),
                'model_version': 'MockDeepfakeDetector_v1.0'
            }
            
        except Exception as e:
            logger.error(f"Error in mock AI analysis: {e}")
            return {'ai_fake_probability': 50.0, 'confidence': 0.5}
    
    def analyze_video(self, video_path):
        """Complete video analysis for deepfake detection"""
        try:
            # Extract video metadata
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            video_info = {
                'fps': fps,
                'frame_count': frame_count,
                'duration': duration,
                'resolution': f"{width}x{height}",
                'file_size': os.path.getsize(video_path)
            }
            
            # Extract frames for analysis
            frames, _, _ = self.extract_frames(video_path)
            
            if not frames:
                return {
                    'error': 'Could not extract frames from video',
                    'fake_probability': 50.0,
                    'video_info': video_info
                }
            
            # Perform various analyses
            face_analysis = self.analyze_face_consistency(frames)
            temporal_analysis = self.analyze_temporal_features(frames)
            ai_analysis = self.mock_ai_analysis(video_info)
            
            # Combine all analysis results
            consistency_weight = 0.3
            temporal_weight = 0.3
            ai_weight = 0.4
            
            # Calculate overall fake probability
            consistency_fake_prob = (1.0 - face_analysis.get('consistency_score', 0.5)) * 100
            temporal_fake_prob = (1.0 - temporal_analysis.get('temporal_score', 0.5)) * 100
            ai_fake_prob = ai_analysis.get('ai_fake_probability', 50.0)
            
            overall_fake_probability = (
                consistency_fake_prob * consistency_weight +
                temporal_fake_prob * temporal_weight +
                ai_fake_prob * ai_weight
            )
            
            # Determine risk level
            if overall_fake_probability >= 70:
                risk_level = "High"
            elif overall_fake_probability >= 40:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            analysis_result = {
                'fake_probability': round(overall_fake_probability, 2),
                'risk_level': risk_level,
                'confidence': ai_analysis.get('confidence', 0.8),
                'video_info': video_info,
                'detailed_analysis': {
                    'face_consistency': face_analysis,
                    'temporal_analysis': temporal_analysis,
                    'ai_analysis': ai_analysis
                },
                'analysis_timestamp': datetime.now().isoformat(),
                'frames_analyzed': len(frames)
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return {
                'error': str(e),
                'fake_probability': 50.0,
                'risk_level': 'Unknown'
            }

# Initialize detector
detector = DeepfakeDetector()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Deepfake Detection API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'Deepfake Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/analyze_video': 'POST - Upload and analyze video for deepfake detection',
            '/health': 'GET - Health check'
        },
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': f"{MAX_FILE_SIZE // (1024*1024)}MB"
    })

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    """
    Analyze uploaded video for deepfake detection
    Expected: multipart/form-data with 'video' file
    """
    try:
        # Check if file is in request
        if 'video' not in request.files:
            return jsonify({
                'error': 'No video file provided',
                'status': 'error'
            }), 400
        
        file = request.files['video']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'status': 'error'
            }), 400
        
        # Validate file type
        if not file.filename or not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not supported. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}',
                'status': 'error'
            }), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        try:
            # Analyze the video
            logger.info(f"Starting analysis of {unique_filename}")
            analysis_result = detector.analyze_video(file_path)
            
            # Add metadata
            analysis_result.update({
                'filename': filename,
                'upload_timestamp': timestamp,
                'file_path': unique_filename,
                'status': 'success'
            })
            
            logger.info(f"Analysis completed for {unique_filename}: {analysis_result.get('fake_probability', 'N/A')}% fake probability")
            
            return jsonify(analysis_result)
            
        finally:
            # Clean up uploaded file
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up file: {unique_filename}")
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up file {unique_filename}: {cleanup_error}")
        
    except Exception as e:
        logger.error(f"Error in analyze_video: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/upload_test', methods=['GET'])
def upload_test():
    """Simple test page for file upload"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Deepfake Detection Test</title></head>
    <body>
        <h2>Video Upload Test</h2>
        <form action="/analyze_video" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/*" required>
            <input type="submit" value="Analyze Video">
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("Starting Deepfake Detection API...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Max file size: {MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"Supported formats: {', '.join(ALLOWED_EXTENSIONS)}")
    
    app.run(debug=True, host='0.0.0.0', port=5001)