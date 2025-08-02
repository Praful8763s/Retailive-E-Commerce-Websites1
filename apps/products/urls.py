from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet
from .retailer_views import RetailerProductViewSet
from .admin_views import AdminProductViewSet

# Public router
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

# Retailer router
retailer_router = DefaultRouter()
retailer_router.register(r'products', RetailerProductViewSet, basename='retailer-product')

# Admin router
admin_router = DefaultRouter()
admin_router.register(r'products', AdminProductViewSet, basename='admin-product')

urlpatterns = [
    path('', include(router.urls)),
    path('retailer/', include(retailer_router.urls)),
    path('admin/', include(admin_router.urls)),
]