from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Q
from .models import Product, Category, ProductReview
from .serializers import ProductSerializer, CategorySerializer, ProductReviewSerializer, ProductCreateSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        """Override list to handle djongo issues"""
        try:
            # Get all categories without complex queries
            categories = list(Category.objects.all())
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Fallback to empty list if there's an error
            return Response([])

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def list(self, request, *args, **kwargs):
        """Override list to handle djongo issues"""
        try:
            # Get all products without complex filtering
            products = list(Product.objects.all())
            # Filter active products in Python instead of database
            active_products = [p for p in products if getattr(p, 'is_active', True)]
            serializer = self.get_serializer(active_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Fallback to empty list if there's an error
            return Response([])
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search products"""
        query = request.query_params.get('q', '')
        try:
            products = list(Product.objects.all())
            if query:
                # Filter in Python to avoid djongo issues
                filtered_products = [
                    p for p in products 
                    if query.lower() in p.name.lower() or query.lower() in p.description.lower()
                ]
            else:
                filtered_products = products
            
            # Only return active products
            active_products = [p for p in filtered_products if getattr(p, 'is_active', True)]
            serializer = self.get_serializer(active_products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response([])
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            product = self.get_object()
            
            # Check if user already reviewed this product
            existing_reviews = list(ProductReview.objects.all())
            user_review = next((r for r in existing_reviews if r.product.id == product.id and r.user.id == request.user.id), None)
            
            if user_review:
                return Response({'error': 'You have already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ProductReviewSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Failed to add review'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)