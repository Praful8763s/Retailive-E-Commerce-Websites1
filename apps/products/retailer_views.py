from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer
from .permissions import IsRetailerOrReadOnly

class RetailerProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for retailers to manage their own products
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsRetailerOrReadOnly]
    
    def get_queryset(self):
        # Retailers can only see their own products
        if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.role == 'retailer':
            return Product.objects.filter(retailer=self.request.user)
        return Product.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        # Automatically set the retailer to the current user
        serializer.save(retailer=self.request.user, is_approved=False)
    
    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """Get products pending admin approval"""
        products = self.get_queryset().filter(is_approved=False)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved_products(self, request):
        """Get approved products"""
        products = self.get_queryset().filter(is_approved=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_stock(self, request, pk=None):
        """Update product stock quantity"""
        product = self.get_object()
        new_stock = request.data.get('stock_quantity')
        
        if new_stock is not None:
            try:
                product.stock_quantity = int(new_stock)
                product.save()
                return Response({'message': 'Stock updated successfully', 'stock_quantity': product.stock_quantity})
            except ValueError:
                return Response({'error': 'Invalid stock quantity'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Stock quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        """Get sales summary for retailer's products"""
        from apps.orders.models import OrderItem
        
        retailer_products = self.get_queryset()
        total_sales = 0
        total_orders = 0
        
        for product in retailer_products:
            order_items = OrderItem.objects.filter(product=product)
            total_orders += order_items.count()
            total_sales += sum(item.quantity * item.price for item in order_items)
        
        return Response({
            'total_products': retailer_products.count(),
            'total_sales': total_sales,
            'total_orders': total_orders,
            'approved_products': retailer_products.filter(is_approved=True).count(),
            'pending_products': retailer_products.filter(is_approved=False).count(),
        })