from rest_framework import permissions

class IsRetailerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow retailers to edit their own products.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated users
        if not request.user.is_authenticated:
            return False
            
        # Check if user is retailer or admin
        if hasattr(request.user, 'userprofile'):
            return request.user.userprofile.role in ['retailer', 'admin']
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin can edit any product
        if request.user.is_staff or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin'):
            return True
        
        # Retailers can only edit their own products
        return obj.retailer == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin users
        return request.user.is_staff or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner of the object
        return obj.user == request.user