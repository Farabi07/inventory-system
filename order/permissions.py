from rest_framework import permissions

class IsCustomerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' and request.user.role.name == 'CUSTOMER'

class IsAdminOrSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name in ['ADMIN', 'SELLER']
