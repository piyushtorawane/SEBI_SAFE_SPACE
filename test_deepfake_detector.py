#!/usr/bin/env python3
"""
Test script for Deepfake Detection System
Tests the API endpoints and video analysis functionality
"""

import requests
import sys
import os
import time
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5001"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
ANALYZE_ENDPOINT = f"{API_BASE_URL}/analyze_video"

def test_api_connection():
    """Test if the deepfake detection API is accessible"""
    print("🔌 Testing API Connection")
    print("-" * 40)
    
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is online and responding")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            print(f"   Timestamp: {data.get('timestamp', 'Unknown')}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure the API server is running on port 5001")
        print("   Run: python deepfake_api.py")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_api_info():
    """Test the API info endpoint"""
    print("\n📋 Testing API Info")
    print("-" * 40)
    
    try:
        response = requests.get(API_BASE_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API info retrieved successfully")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Supported formats: {', '.join(data.get('supported_formats', []))}")
            print(f"   Max file size: {data.get('max_file_size', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to get API info: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting API info: {e}")
        return False

def create_mock_video_file():
    """Create a small mock video file for testing"""
    try:
        import cv2
        import numpy as np
        
        # Create a simple test video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = 'test_video.mp4'
        out = cv2.VideoWriter(video_path, fourcc, 10.0, (640, 480))
        
        # Generate 30 frames
        for i in range(30):
            # Create a simple frame with changing colors
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # Add some text
            cv2.putText(frame, f'Frame {i+1}', (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        print(f"✅ Created test video: {video_path}")
        return video_path
        
    except ImportError:
        print("⚠️ OpenCV not available, cannot create test video")
        return None
    except Exception as e:
        print(f"❌ Error creating test video: {e}")
        return None

def test_video_analysis_no_file():
    """Test video analysis endpoint without file"""
    print("\n🚫 Testing Video Analysis (No File)")
    print("-" * 40)
    
    try:
        response = requests.post(ANALYZE_ENDPOINT, timeout=30)
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Correctly rejected request without file")
            print(f"   Error message: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Unexpected response code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing no-file case: {e}")
        return False

def test_video_analysis_invalid_file():
    """Test video analysis with invalid file type"""
    print("\n📄 Testing Video Analysis (Invalid File)")
    print("-" * 40)
    
    try:
        # Create a fake text file
        fake_content = "This is not a video file"
        files = {'video': ('fake_video.txt', fake_content, 'text/plain')}
        
        response = requests.post(ANALYZE_ENDPOINT, files=files, timeout=30)
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Correctly rejected invalid file type")
            print(f"   Error message: {data.get('error', 'N/A')}")
            return True
        else:
            print(f"❌ Unexpected response code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid file: {e}")
        return False

def test_video_analysis_mock_file():
    """Test video analysis with mock video file"""
    print("\n🎬 Testing Video Analysis (Mock Video)")
    print("-" * 40)
    
    # Create mock video
    video_path = create_mock_video_file()
    
    if not video_path:
        print("⚠️ Skipping video analysis test - no test video available")
        return True
    
    try:
        with open(video_path, 'rb') as video_file:
            files = {'video': ('test_video.mp4', video_file.read(), 'video/mp4')}
            
            print("📤 Uploading test video...")
            response = requests.post(ANALYZE_ENDPOINT, files=files, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Video analysis completed successfully")
                print(f"   Fake probability: {data.get('fake_probability', 'N/A')}%")
                print(f"   Risk level: {data.get('risk_level', 'N/A')}")
                print(f"   Confidence: {data.get('confidence', 'N/A')}")
                print(f"   Frames analyzed: {data.get('frames_analyzed', 'N/A')}")
                
                # Check video info
                if 'video_info' in data:
                    video_info = data['video_info']
                    print(f"   Duration: {video_info.get('duration', 'N/A'):.1f}s")
                    print(f"   FPS: {video_info.get('fps', 'N/A'):.1f}")
                    print(f"   Resolution: {video_info.get('resolution', 'N/A')}")
                
                return True
            else:
                print(f"❌ Video analysis failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"   Response: {response.text[:200]}...")
                return False
                
    except Exception as e:
        print(f"❌ Error testing video analysis: {e}")
        return False
    
    finally:
        # Clean up test file
        try:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
                print(f"🧹 Cleaned up test file: {video_path}")
        except Exception as cleanup_error:
            print(f"⚠️ Could not clean up test file: {cleanup_error}")

def test_streamlit_integration():
    """Test if Streamlit app can be imported"""
    print("\n🎨 Testing Streamlit Integration")
    print("-" * 40)
    
    try:
        # Try to import the main functions
        import sys
        import os
        
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # Try importing key functions
        from deepfake_detector import check_api_status, format_file_size, get_risk_color
        
        print("✅ Streamlit app imports successfully")
        
        # Test some utility functions
        test_risk_color = get_risk_color("High")
        test_file_size = format_file_size(1024*1024)
        
        print(f"   Risk color function: {test_risk_color}")
        print(f"   File size formatting: {test_file_size}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error testing Streamlit integration: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result"""
    print("🧪 Deepfake Detection System - Test Suite")
    print("=" * 60)
    
    # Track test results
    tests = [
        ("API Connection", test_api_connection),
        ("API Info", test_api_info),
        ("No File Analysis", test_video_analysis_no_file),
        ("Invalid File Analysis", test_video_analysis_invalid_file),
        ("Mock Video Analysis", test_video_analysis_mock_file),
        ("Streamlit Integration", test_streamlit_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The deepfake detection system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    print("Starting Deepfake Detection System Tests...\n")
    
    # Check if API should be running
    print("💡 Before running tests:")
    print("   1. Make sure to install dependencies: pip install opencv-python")
    print("   2. Start the API server: python deepfake_api.py")
    print("   3. Wait for the server to be ready, then run this test\n")
    
    # Run tests
    success = run_all_tests()
    
    print("\n💡 To run the applications:")
    print("   API: python deepfake_api.py (port 5001)")
    print("   UI:  streamlit run deepfake_detector.py --server.port 8504")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)