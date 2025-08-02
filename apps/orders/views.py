from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, Cart, CartItem, OrderItem
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer, OrderCreateSerializer
from apps.products.models import Product

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        try:
            # Get all orders and filter in Python
            all_orders = list(Order.objects.all())
            user_orders = [order for order in all_orders if order.user.id == self.request.user.id]
            return user_orders
        except Exception:
            return []
    
    def list(self, request, *args, **kwargs):
        """Override list to handle djongo issues"""
        try:
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data)
        except Exception:
            return Response([])
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Get or create cart
                all_carts = list(Cart.objects.all())
                user_cart = next((cart for cart in all_carts if cart.user.id == request.user.id), None)
                
                if not user_cart:
                    user_cart = Cart.objects.create(user=request.user)
                
                # Get cart items
                all_cart_items = list(CartItem.objects.all())
                cart_items = [item for item in all_cart_items if item.cart.id == user_cart.id]
                
                if not cart_items:
                    return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Calculate total
                total_amount = sum(item.quantity * item.product.price for item in cart_items)
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    shipping_address=serializer.validated_data['shipping_address']
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                # Clear cart items
                for item in cart_items:
                    item.delete()
                
                # Send confirmation email
                try:
                    send_mail(
                        'Order Confirmation - RetailHive',
                        f'Your order #{order.id} has been placed successfully. Total: ${order.total_amount}',
                        settings.EMAIL_HOST_USER,
                        [request.user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Email sending failed: {e}")
                
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Failed to create order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    try:
        # Get or create cart
        all_carts = list(Cart.objects.all())
        user_cart = next((cart for cart in all_carts if cart.user.id == request.user.id), None)
        
        if not user_cart:
            user_cart = Cart.objects.create(user=request.user)
        
        serializer = CartSerializer(user_cart)
        return Response(serializer.data)
    except Exception as e:
        # Return empty cart if there's an error
        return Response({
            'id': None,
            'items': [],
            'total_items': 0,
            'total_price': 0,
            'created_at': None
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        # Get or create cart
        all_carts = list(Cart.objects.all())
        user_cart = next((cart for cart in all_carts if cart.user.id == request.user.id), None)
        
        if not user_cart:
            user_cart = Cart.objects.create(user=request.user)
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get product
        all_products = list(Product.objects.all())
        product = next((p for p in all_products if p.id == int(product_id) and getattr(p, 'is_active', True)), None)
        
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.stock_quantity < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if item already in cart
        all_cart_items = list(CartItem.objects.all())
        existing_item = next((item for item in all_cart_items if item.cart.id == user_cart.id and item.product.id == product.id), None)
        
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            existing_item.quantity = new_quantity
            existing_item.save()
            cart_item = existing_item
        else:
            cart_item = CartItem.objects.create(
                cart=user_cart,
                product=product,
                quantity=quantity
            )
        
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': 'Failed to add to cart'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        # Get user's cart
        all_carts = list(Cart.objects.all())
        user_cart = next((cart for cart in all_carts if cart.user.id == request.user.id), None)
        
        if not user_cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get cart item
        all_cart_items = list(CartItem.objects.all())
        cart_item = next((item for item in all_cart_items if item.id == int(item_id) and item.cart.id == user_cart.id), None)
        
        if not cart_item:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Failed to remove item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)