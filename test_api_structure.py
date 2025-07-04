#!/usr/bin/env python3
"""Test script to verify API structure without database."""

import json

import requests

BASE_URL = "http://localhost:8000"

def test_endpoint(method, path, description, data=None):
    """Test an endpoint and print results."""
    url = f"{BASE_URL}{path}"
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"Status: {response.status_code}")
        if response.status_code < 500:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all API structure tests."""
    print("API Structure Test - The Sauce Bottle")
    print("="*60)
    
    # Test root endpoint
    test_endpoint("GET", "/", "Root endpoint")
    
    # Test health endpoints
    test_endpoint("GET", "/api/health", "Health check")
    test_endpoint("GET", "/api/health/db", "Database health check")
    
    # Test API v1 info
    test_endpoint("GET", "/api/v1/", "API v1 info")
    
    # Test documentation endpoints
    print(f"\n{'='*60}")
    print("Documentation URLs:")
    print(f"Swagger UI: {BASE_URL}/api/docs")
    print(f"ReDoc: {BASE_URL}/api/redoc")
    print(f"OpenAPI Schema: {BASE_URL}/api/openapi.json")
    
    # Test politicians endpoints (will fail without DB but shows structure)
    test_endpoint("GET", "/api/v1/politicians/", "List politicians")
    
    # Test statements endpoints (will fail without DB but shows structure)
    test_endpoint("GET", "/api/v1/statements/", "List statements")

if __name__ == "__main__":
    main()
