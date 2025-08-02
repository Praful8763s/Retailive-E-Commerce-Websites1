#!/usr/bin/env python
"""
Test script to verify registration functionality
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

from django.contrib.auth.models import User
from apps.users.serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token

def test_customer_registration():
    """Test customer registration"""
    print("🧪 Testing customer registration...")
    
    data = {
        'username': 'test_customer',
        'email': 'test_customer@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Customer',
        'role': 'customer'
    }
    
    try:
        # Clean up existing user
        User.objects.filter(username='test_customer').delete()
        
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            print(f"✅ Customer registration successful!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.userprofile.role}")
            print(f"   Token: {token.key[:20]}...")
            
            # Clean up
            user.delete()
            return True
        else:
            print(f"❌ Customer registration failed: {serializer.errors}")
            return False
    except Exception as e:
        print(f"❌ Customer registration error: {e}")
        return False

def test_retailer_registration():
    """Test retailer registration"""
    print("\n🧪 Testing retailer registration...")
    
    data = {
        'username': 'test_retailer',
        'email': 'test_retailer@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Retailer',
        'role': 'retailer',
        'business_name': 'Test Store',
        'business_license': 'TEST123'
    }
    
    try:
        # Clean up existing user
        User.objects.filter(username='test_retailer').delete()
        
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            print(f"✅ Retailer registration successful!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.userprofile.role}")
            print(f"   Business: {user.userprofile.business_name}")
            print(f"   Token: {token.key[:20]}...")
            
            # Clean up
            user.delete()
            return True
        else:
            print(f"❌ Retailer registration failed: {serializer.errors}")
            return False
    except Exception as e:
        print(f"❌ Retailer registration error: {e}")
        return False

def test_validation_errors():
    """Test validation errors"""
    print("\n🧪 Testing validation errors...")
    
    # Test password mismatch
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'testpass123',
        'password_confirm': 'different_pass',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'customer'
    }
    
    serializer = UserRegistrationSerializer(data=data)
    if not serializer.is_valid():
        print("✅ Password mismatch validation working")
    else:
        print("❌ Password mismatch validation failed")
    
    # Test retailer without business name
    data = {
        'username': 'test_retailer2',
        'email': 'test2@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Retailer',
        'role': 'retailer',
        'business_name': ''  # Empty business name
    }
    
    serializer = UserRegistrationSerializer(data=data)
    if not serializer.is_valid():
        print("✅ Business name validation working")
    else:
        print("❌ Business name validation failed")

if __name__ == "__main__":
    print("🚀 Starting registration tests...")
    
    customer_ok = test_customer_registration()
    retailer_ok = test_retailer_registration()
    test_validation_errors()
    
    print(f"\n📊 Test Results:")
    print(f"   Customer Registration: {'✅ PASS' if customer_ok else '❌ FAIL'}")
    print(f"   Retailer Registration: {'✅ PASS' if retailer_ok else '❌ FAIL'}")
    
    if customer_ok and retailer_ok:
        print("\n🎉 All registration tests passed! Registration is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")