#!/usr/bin/env python3
"""
Test script for BSE Announcement Analyzer
Tests credibility analysis and mismatch detection functionality
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_credibility_analysis():
    """Test the credibility analysis functionality"""
    
    try:
        from announcement_analyzer import AnnouncementAnalyzer
        
        print("🔍 BSE Announcement Analyzer - Test Results")
        print("=" * 60)
        
        # Initialize analyzer
        analyzer = AnnouncementAnalyzer()
        
        # Test cases with expected outcomes
        test_cases = [
            {
                "company": "Reliance Industries",
                "announcement": "Reliance Industries reports record profit of ₹15,000 crores with exceptional growth",
                "expected_credibility": "Low",  # Should be low due to recent negative history
                "description": "Record profit claim after recent losses"
            },
            {
                "company": "TCS", 
                "announcement": "TCS announces massive loss of ₹2,000 crores due to market challenges",
                "expected_credibility": "Medium",
                "description": "Loss announcement with some historical context"
            },
            {
                "company": "HDFC Bank",
                "announcement": "HDFC Bank board meeting scheduled for dividend declaration",
                "expected_credibility": "High", 
                "description": "Neutral corporate governance announcement"
            },
            {
                "company": "New Company",
                "announcement": "New Company reports steady quarterly growth",
                "expected_credibility": "Medium",
                "description": "New company with no historical data"
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📊 Test Case {i}: {test_case['description']}")
            print(f"Company: {test_case['company']}")
            print(f"Announcement: \"{test_case['announcement'][:80]}{'...' if len(test_case['announcement']) > 80 else ''}\"")
            
            # Perform credibility analysis
            credibility, reason, score = analyzer.check_credibility_mismatch(
                test_case['company'], 
                test_case['announcement']
            )
            
            # Check result
            passed = credibility == test_case['expected_credibility']
            status = "✅ PASS" if passed else "❌ FAIL"
            
            print(f"Expected: {test_case['expected_credibility']}")
            print(f"Actual: {credibility} (Score: {score})")
            print(f"Reason: {reason}")
            print(f"Status: {status}")
            
            if not passed:
                all_passed = False
        
        print("\n" + "=" * 60)
        final_status = "✅ ALL CREDIBILITY TESTS PASSED" if all_passed else "❌ SOME CREDIBILITY TESTS FAILED"
        print(f"Credibility Analysis Result: {final_status}")
        
        return all_passed
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure announcement_analyzer.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis functionality"""
    
    try:
        from announcement_analyzer import AnnouncementAnalyzer
        
        print("\n📈 Sentiment Analysis Test")
        print("-" * 40)
        
        analyzer = AnnouncementAnalyzer()
        
        sentiment_test_cases = [
            ("Record profit with exceptional growth", "positive"),
            ("Massive loss due to market downturn", "negative"), 
            ("Board meeting for dividend declaration", "neutral"),
            ("Tremendous growth and outstanding performance", "positive"),
            ("Financial crisis and significant decline", "negative")
        ]
        
        all_passed = True
        
        for text, expected_sentiment in sentiment_test_cases:
            sentiment, score, keywords = analyzer.analyze_announcement_sentiment(text)
            passed = sentiment == expected_sentiment
            status = "✅" if passed else "❌"
            
            print(f"{status} '{text[:40]}...' -> {sentiment} (expected: {expected_sentiment})")
            print(f"    Score: {score}, Keywords: {len(keywords)}")
            
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Sentiment Test Error: {e}")
        return False

def test_data_fetching():
    """Test announcement data fetching"""
    
    try:
        from announcement_analyzer import AnnouncementAnalyzer
        
        print("\n🔄 Data Fetching Test")
        print("-" * 30)
        
        analyzer = AnnouncementAnalyzer()
        
        # Test historical data loading
        print(f"✅ Historical data loaded: {len(analyzer.historical_announcements)} records")
        
        # Test announcement fetching
        announcements = analyzer.fetch_latest_announcements()
        print(f"✅ Latest announcements fetched: {len(announcements)} records")
        
        if announcements:
            print("Sample announcement:")
            sample = announcements[0]
            print(f"  Company: {sample['Company']}")
            print(f"  Date: {sample['Date']}")
            print(f"  Text: {sample['AnnouncementText'][:60]}...")
        
        # Test full analysis
        analyzed_data = analyzer.analyze_all_announcements(announcements)
        print(f"✅ Analysis completed: {len(analyzed_data)} records processed")
        
        if not analyzed_data.empty:
            credibility_distribution = analyzed_data['CredibilityLevel'].value_counts()
            print("Credibility distribution:")
            for level, count in credibility_distribution.items():
                print(f"  {level}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data Fetching Test Error: {e}")
        return False

def test_historical_comparison():
    """Test historical comparison logic"""
    
    try:
        from announcement_analyzer import AnnouncementAnalyzer
        import pandas as pd
        
        print("\n📚 Historical Comparison Test")
        print("-" * 35)
        
        analyzer = AnnouncementAnalyzer()
        
        # Test with a company that has historical data
        test_company = "Reliance Industries"
        historical_data = analyzer.historical_announcements[
            analyzer.historical_announcements["Company"] == test_company
        ]
        
        print(f"Historical records for {test_company}: {len(historical_data)}")
        
        if not historical_data.empty:
            # Show recent sentiment trend
            recent_sentiments = historical_data["Sentiment"].tail(5).tolist()
            print(f"Recent sentiment trend: {recent_sentiments}")
            
            # Test mismatch detection
            positive_after_negative = "Record profit with exceptional performance and highest revenue ever"
            credibility, reason, score = analyzer.check_credibility_mismatch(test_company, positive_after_negative)
            
            print(f"\nMismatch Test Result:")
            print(f"Announcement: {positive_after_negative[:50]}...")
            print(f"Credibility: {credibility}")
            print(f"Reason: {reason}")
            print(f"Score: {score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Historical Comparison Test Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting BSE Announcement Analyzer Tests...\n")
    
    # Run all tests
    credibility_tests = test_credibility_analysis()
    sentiment_tests = test_sentiment_analysis()
    data_tests = test_data_fetching()
    historical_tests = test_historical_comparison()
    
    # Overall result
    print("\n" + "=" * 60)
    if all([credibility_tests, sentiment_tests, data_tests, historical_tests]):
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The BSE Announcement Analyzer is working correctly.")
    else:
        print("⚠️ SOME TESTS FAILED!")
        print("Please check the implementation.")
    
    print("\n💡 To run the dashboard:")
    print("streamlit run announcement_analyzer.py --server.port 8503")
    print("\nThe dashboard will be available at: http://localhost:8503")