#!/usr/bin/env python
"""
Test script to verify all API endpoints work correctly
"""
import os
import sys
import django
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retailhive.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_registration_endpoint():
    """Test the registration API endpoint"""
    print("🧪 Testing registration endpoint...")
    
    client = Client()
    
    # Test customer registration
    customer_data = {
        'username': 'api_test_customer',
        'email': 'api_customer@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'API',
        'last_name': 'Customer',
        'role': 'customer'
    }
    
    try:
        # Clean up existing user
        User.objects.filter(username='api_test_customer').delete()
        
        response = client.post('/api/users/register/', 
                             data=json.dumps(customer_data),
                             content_type='application/json')
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Customer registration endpoint working")
            print(f"   Status: {response.status_code}")
            print(f"   User: {data['user']['username']}")
            print(f"   Token: {data['token'][:20]}...")
            
            # Clean up
            User.objects.filter(username='api_test_customer').delete()
            return True
        else:
            print(f"❌ Customer registration failed: {response.status_code}")
            print(f"   Response: {response.content.decode()}")
            return False
    except Exception as e:
        print(f"❌ Customer registration error: {e}")
        return False

def test_login_endpoint():
    """Test the login API endpoint"""
    print("\n🧪 Testing login endpoint...")
    
    client = Client()
    
    # Create a test user first
    try:
        User.objects.filter(username='login_test_user').delete()
        user = User.objects.create_user(
            username='login_test_user',
            email='login_test@example.com',
            password='testpass123'
        )
        
        login_data = {
            'username': 'login_test_user',
            'password': 'testpass123'
        }
        
        response = client.post('/api/users/login/',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login endpoint working")
            print(f"   Status: {response.status_code}")
            print(f"   User: {data['user']['username']}")
            print(f"   Token: {data['token'][:20]}...")
            
            # Clean up
            user.delete()
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.content.decode()}")
            user.delete()
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_products_endpoint():
    """Test the products API endpoint"""
    print("\n🧪 Testing products endpoint...")
    
    client = Client()
    
    try:
        response = client.get('/api/products/products/')
        
        if response.status_code == 200:
            data = response.json()
            products_count = len(data) if isinstance(data, list) else len(data.get('results', []))
            print(f"✅ Products endpoint working")
            print(f"   Status: {response.status_code}")
            print(f"   Products found: {products_count}")
            return True
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Products endpoint error: {e}")
        return False

def test_categories_endpoint():
    """Test the categories API endpoint"""
    print("\n🧪 Testing categories endpoint...")
    
    client = Client()
    
    try:
        response = client.get('/api/products/categories/')
        
        if response.status_code == 200:
            data = response.json()
            categories_count = len(data) if isinstance(data, list) else len(data.get('results', []))
            print(f"✅ Categories endpoint working")
            print(f"   Status: {response.status_code}")
            print(f"   Categories found: {categories_count}")
            return True
        else:
            print(f"❌ Categories endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting API endpoint tests...")
    
    registration_ok = test_registration_endpoint()
    login_ok = test_login_endpoint()
    products_ok = test_products_endpoint()
    categories_ok = test_categories_endpoint()
    
    print(f"\n📊 API Test Results:")
    print(f"   Registration Endpoint: {'✅ PASS' if registration_ok else '❌ FAIL'}")
    print(f"   Login Endpoint: {'✅ PASS' if login_ok else '❌ FAIL'}")
    print(f"   Products Endpoint: {'✅ PASS' if products_ok else '❌ FAIL'}")
    print(f"   Categories Endpoint: {'✅ PASS' if categories_ok else '❌ FAIL'}")
    
    all_passed = all([registration_ok, login_ok, products_ok, categories_ok])
    
    if all_passed:
        print("\n🎉 All API endpoints are working correctly!")
        print("✅ Registration page will work perfectly with the backend!")
    else:
        print("\n⚠️ Some API endpoints failed. Check the errors above.")