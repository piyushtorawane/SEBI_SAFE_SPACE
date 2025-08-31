#!/usr/bin/env python3
"""
Test script for Fraud Content Scanner
Tests various text samples to verify fraud detection functionality
"""

import sys
import os

# Add the current directory to Python path to import fraud_scanner
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fraud_scanner import analyze_text_for_fraud, get_risk_color

def test_fraud_detection():
    """Test the fraud detection functionality with sample texts"""
    
    # Test cases with expected risk levels
    test_cases = [
        {
            "text": "This investment guarantees 50% returns in just 30 days with absolutely no risk involved!",
            "expected_risk": "High",
            "description": "High risk - multiple guaranteed/no risk claims"
        },
        {
            "text": "Get this hot tip for exclusive opportunity - limited time offer to make quick money!",
            "expected_risk": "Medium", 
            "description": "Medium risk - urgency and exclusivity claims"
        },
        {
            "text": "This looks like a good investment opportunity with potential gains in technology.",
            "expected_risk": "Low",
            "description": "Low risk - general investment language"
        },
        {
            "text": "Hello, how are you today? The weather is nice.",
            "expected_risk": "Low",
            "description": "No risk - normal conversation"
        },
        {
            "text": "GUARANTEED RETURNS! SURE SHOT TIP! IPO ALLOTMENT GUARANTEED! DOUBLES YOUR MONEY!",
            "expected_risk": "High",
            "description": "High risk - multiple high-risk keywords"
        }
    ]
    
    print("🛡️ Fraud Content Scanner - Test Results")
    print("=" * 60)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['description']}")
        print(f"Input: \"{test_case['text'][:50]}{'...' if len(test_case['text']) > 50 else ''}\"")
        
        # Analyze the text
        result = analyze_text_for_fraud(test_case['text'])
        
        # Check if result matches expected
        passed = result['risk_level'] == test_case['expected_risk']
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"Expected: {test_case['expected_risk']}")
        print(f"Actual: {result['risk_level']} (Score: {result['risk_score']})")
        print(f"Status: {status}")
        
        if result['detected_keywords']:
            print(f"Keywords found: {len(result['detected_keywords'])}")
            for kw in result['detected_keywords'][:3]:  # Show first 3
                print(f"  - '{kw['keyword']}' (risk: {kw['risk_value']}, count: {kw['count']})")
        
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    final_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
    print(f"Final Result: {final_status}")
    
    return all_passed

def test_url_detection():
    """Test URL detection functionality"""
    from fraud_scanner import is_url
    
    print("\n🔗 URL Detection Test")
    print("-" * 30)
    
    url_test_cases = [
        ("https://example.com", True),
        ("http://test.org", True),
        ("ftp://files.com", True),
        ("just some text", False),
        ("not a url at all", False),
        ("", False)
    ]
    
    all_passed = True
    
    for url, expected in url_test_cases:
        result = is_url(url)
        passed = result == expected
        status = "✅" if passed else "❌"
        print(f"{status} '{url}' -> {result} (expected: {expected})")
        
        if not passed:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("Starting Fraud Content Scanner Tests...\n")
    
    # Run fraud detection tests
    fraud_tests_passed = test_fraud_detection()
    
    # Run URL detection tests  
    url_tests_passed = test_url_detection()
    
    # Overall result
    print("\n" + "=" * 60)
    if fraud_tests_passed and url_tests_passed:
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The Fraud Content Scanner is working correctly.")
    else:
        print("⚠️ SOME TESTS FAILED!")
        print("Please check the implementation.")
    
    print("\n💡 To run the app:")
    print("streamlit run fraud_scanner.py --server.port 8502")