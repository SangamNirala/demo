"""
API Test Script
===============

This script tests the backend API endpoints to ensure everything is working correctly.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_student(roll_no="2023BT2086"):
    """Test get student endpoint"""
    print("\n" + "="*60)
    print(f"Testing Get Student Endpoint (Roll No: {roll_no})")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/student/{roll_no}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nStudent Found:")
            print(f"  Name: {data.get('name')}")
            print(f"  Roll No: {data.get('roll_no')}")
            print(f"  Course: {data.get('course')}")
            print(f"  Year: {data.get('year_string')}")
            print(f"  Attendance: {data.get('attendance_percentage')}%")
            print(f"  CGPA: {data.get('cgpa_current')}")
        else:
            print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction(roll_no="2023BT2086"):
    """Test prediction endpoint"""
    print("\n" + "="*60)
    print(f"Testing Prediction Endpoint (Roll No: {roll_no})")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/api/predict/{roll_no}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('error'):
                print(f"❌ Prediction Error: {data.get('message')}")
                return False
            
            print(f"\n✅ Prediction Successful!")
            print(f"\nStudent: {data.get('student_info', {}).get('name')}")
            print(f"Risk Level: {data.get('risk_level')} ({data.get('risk_percentage')}%)")
            
            print(f"\nTop Risk Factors:")
            for factor in data.get('risk_factors', [])[:3]:
                print(f"  - {factor.get('name')}: {factor.get('contribution')}%")
            
            print(f"\nRecommendations:")
            for rec in data.get('recommendations', [])[:3]:
                print(f"  {rec.get('icon')} {rec.get('title')}")
        else:
            print(f"Response: {response.json()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 BACKEND API TEST SUITE")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the backend server is running!")
    
    results = {
        'Health Check': test_health(),
        'Get Student': test_get_student(),
        'Prediction': test_prediction()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
