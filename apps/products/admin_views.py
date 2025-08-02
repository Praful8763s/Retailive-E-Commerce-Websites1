from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer
from .permissions import IsAdminOrReadOnly

class AdminProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for admins to manage all products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """Get all products pending approval"""
        products = Product.objects.filter(is_approved=False)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def approve_product(self, request, pk=None):
        """Approve a product"""
        product = self.get_object()
        product.is_approved = True
        product.save()
        
        # Send notification to retailer (you can implement email notification here)
        return Response({
            'message': 'Product approved successfully',
            'product_id': product.id,
            'product_name': product.name
        })
    
    @action(detail=True, methods=['patch'])
    def reject_product(self, request, pk=None):
        """Reject a product"""
        product = self.get_object()
        rejection_reason = request.data.get('reason', 'No reason provided')
        
        product.is_approved = False
        product.is_active = False
        product.save()
        
        # You can store rejection reason in a separate model if needed
        return Response({
            'message': 'Product rejected',
            'product_id': product.id,
            'reason': rejection_reason
        })
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for admin"""
        from apps.orders.models import Order, OrderItem
        from apps.users.models import UserProfile
        
        total_products = Product.objects.count()
        approved_products = Product.objects.filter(is_approved=True).count()
        pending_products = Product.objects.filter(is_approved=False).count()
        
        total_orders = Order.objects.count()
        total_customers = UserProfile.objects.filter(role='customer').count()
        total_retailers = UserProfile.objects.filter(role='retailer').count()
        
        # Top selling products
        top_products = Product.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:5]
        
        return Response({
            'products': {
                'total': total_products,
                'approved': approved_products,
                'pending': pending_products,
            },
            'users': {
                'customers': total_customers,
                'retailers': total_retailers,
            },
            'orders': {
                'total': total_orders,
            },
            'top_products': ProductSerializer(top_products, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def retailer_products(self, request):
        """Get products by retailer"""
        retailer_id = request.query_params.get('retailer_id')
        if retailer_id:
            products = Product.objects.filter(retailer_id=retailer_id)
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        
        return Response({'error': 'retailer_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'])
    def bulk_approve(self, request):
        """Bulk approve products"""
        product_ids = request.data.get('product_ids', [])
        if not product_ids:
            return Response({'error': 'product_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = Product.objects.filter(id__in=product_ids).update(is_approved=True)
        
        return Response({
            'message': f'{updated_count} products approved successfully',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['patch'])
    def bulk_reject(self, request):
        """Bulk reject products"""
        product_ids = request.data.get('product_ids', [])
        if not product_ids:
            return Response({'error': 'product_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_count = Product.objects.filter(id__in=product_ids).update(
            is_approved=False, 
            is_active=False
        )
        
        return Response({
            'message': f'{updated_count} products rejected successfully',
            'updated_count': updated_count
        })