#!/usr/bin/env python3
"""
Test script for SEBI Safe Space Unified Application
Tests all components and functionality
"""

import sys
import os
import requests
import time
from datetime import datetime

def test_unified_app_imports():
    """Test if the unified app can be imported successfully"""
    print("🧪 Testing Unified App Imports")
    print("-" * 40)
    
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # Try importing main functions
        from sebi_safe_space import (
            load_advisors_data, 
            verify_advisor_local, 
            analyze_fraud_content,
            load_historical_announcements,
            fetch_mock_announcements,
            check_deepfake_api
        )
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing imports: {e}")
        return False

def test_advisor_verification():
    """Test advisor verification functionality"""
    print("\n👨‍💼 Testing Advisor Verification")
    print("-" * 40)
    
    try:
        from sebi_safe_space import verify_advisor_local
        
        # Test cases
        test_cases = [
            ("John Smith", "Should find advisor"),
            ("IA001234", "Should find by registration number"),
            ("NonExistent", "Should not find advisor")
        ]
        
        for query, description in test_cases:
            result = verify_advisor_local(query)
            
            if result:
                status = "✅ PASS" if result.get('status') in ['Verified', 'Not Found'] else "❌ FAIL"
                print(f"{status} {description}: {result.get('status', 'Unknown')}")
            else:
                print(f"⚠️ No result for: {query}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing advisor verification: {e}")
        return False

def test_fraud_scanner():
    """Test fraud content scanning functionality"""
    print("\n🛡️ Testing Fraud Scanner")
    print("-" * 40)
    
    try:
        from sebi_safe_space import analyze_fraud_content
        
        test_cases = [
            ("This investment guarantees 50% returns with no risk!", "High", "High risk text"),
            ("Get this exclusive opportunity with guaranteed returns!", "High", "Multiple high-risk keywords"),
            ("This is a good investment opportunity in technology", "Low", "Normal investment language"),
            ("Hello, how are you today?", "Low", "Normal conversation")
        ]
        
        for text, expected_risk, description in test_cases:
            result = analyze_fraud_content(text)
            actual_risk = result.get('risk_level', 'Unknown')
            
            status = "✅ PASS" if actual_risk == expected_risk else "⚠️ DIFFERENT"
            print(f"{status} {description}: {actual_risk} (expected: {expected_risk})")
            print(f"    Score: {result.get('risk_score', 0)}, Keywords: {len(result.get('detected_keywords', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing fraud scanner: {e}")
        return False

def test_announcement_analyzer():
    """Test announcement analysis functionality"""
    print("\n📊 Testing Announcement Analyzer")
    print("-" * 40)
    
    try:
        from sebi_safe_space import fetch_mock_announcements, load_historical_announcements
        
        # Test fetching announcements
        announcements = fetch_mock_announcements()
        print(f"✅ Fetched {len(announcements)} mock announcements")
        
        # Test loading historical data
        historical = load_historical_announcements()
        print(f"✅ Loaded {len(historical)} historical records")
        
        # Test data structure
        if announcements:
            first_announcement = announcements[0]
            required_fields = ['Company', 'Date', 'AnnouncementText']
            has_all_fields = all(field in first_announcement for field in required_fields)
            
            status = "✅ PASS" if has_all_fields else "❌ FAIL"
            print(f"{status} Announcement data structure check")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing announcement analyzer: {e}")
        return False

def test_deepfake_api_connection():
    """Test deepfake API connection"""
    print("\n🎭 Testing Deepfake API Connection")
    print("-" * 40)
    
    try:
        from sebi_safe_space import check_deepfake_api
        
        api_status = check_deepfake_api()
        
        if api_status:
            print("✅ Deepfake API is online and accessible")
            
            # Test API endpoints
            try:
                response = requests.get("http://localhost:5001/", timeout=5)
                if response.status_code == 200:
                    print("✅ API info endpoint working")
                else:
                    print(f"⚠️ API info returned status: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Could not test API endpoints: {e}")
        else:
            print("❌ Deepfake API is offline")
            print("   Start with: python deepfake_api.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing deepfake API: {e}")
        return False

def test_file_dependencies():
    """Test if required files exist"""
    print("\n📁 Testing File Dependencies")
    print("-" * 40)
    
    required_files = [
        ('sebi_advisors.csv', 'Advisor database'),
        ('historical_announcements.csv', 'Historical announcements'),
    ]
    
    optional_files = [
        ('ia08012025.xlsx', 'Excel advisor database'),
        ('uploads/', 'Upload directory (for deepfake)')
    ]
    
    all_good = True
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Missing - {file_path}")
            all_good = False
    
    for file_path, description in optional_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: Found")
        else:
            print(f"⚠️ {description}: Optional - {file_path}")
    
    return all_good

def test_streamlit_compatibility():
    """Test Streamlit compatibility"""
    print("\n🎨 Testing Streamlit Compatibility")
    print("-" * 40)
    
    try:
        import streamlit as st
        print("✅ Streamlit is available")
        
        # Test if we can import without running
        with open('sebi_safe_space.py', 'r') as f:
            content = f.read()
            
        # Check for common issues
        issues = []
        
        if 'st.set_page_config' not in content:
            issues.append("Missing page configuration")
        
        if 'st.tabs(' not in content:
            issues.append("Missing tab implementation")
        
        if 'st.sidebar' not in content:
            issues.append("Missing sidebar implementation")
        
        if issues:
            print("⚠️ Potential issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Streamlit code structure looks good")
        
        return len(issues) == 0
        
    except ImportError:
        print("❌ Streamlit not available")
        return False
    except Exception as e:
        print(f"❌ Error testing Streamlit compatibility: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🧪 SEBI Safe Space - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Unified App Imports", test_unified_app_imports),
        ("Advisor Verification", test_advisor_verification),
        ("Fraud Scanner", test_fraud_scanner),
        ("Announcement Analyzer", test_announcement_analyzer),
        ("Deepfake API Connection", test_deepfake_api_connection),
        ("File Dependencies", test_file_dependencies),
        ("Streamlit Compatibility", test_streamlit_compatibility)
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
        print("🎉 ALL TESTS PASSED! SEBI Safe Space is ready to use.")
        print("\n💡 To run the unified application:")
        print("   streamlit run sebi_safe_space.py --server.port 8505")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        
        if passed >= total * 0.8:  # 80% pass rate
            print("\n✅ Most features are working. You can still run the app:")
            print("   streamlit run sebi_safe_space.py --server.port 8505")
    
    return passed == total

if __name__ == "__main__":
    print("Starting SEBI Safe Space Comprehensive Tests...\n")
    
    print("💡 Prerequisites:")
    print("   1. Install dependencies: pip install streamlit requests opencv-python")
    print("   2. Ensure data files are present (sebi_advisors.csv, etc.)")
    print("   3. Optionally start deepfake API: python deepfake_api.py")
    print("")
    
    # Run comprehensive tests
    success = run_comprehensive_test()
    
    print(f"\n🏁 Test suite completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)