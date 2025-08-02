from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from apps.products.models import Product, Category
from .models import Order, Cart, CartItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category=self.category,
            stock_quantity=10
        )
    
    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), "testuser's Cart")
    
    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=99.99,
            shipping_address="123 Test St"
        )
        self.assertEqual(order.status, 'pending')
        self.assertEqual(str(order), "Order #1 - testuser")

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category=self.category,
            stock_quantity=10
        )
    
    def test_get_cart_unauthenticated(self):
        response = self.client.get('/api/orders/cart/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)