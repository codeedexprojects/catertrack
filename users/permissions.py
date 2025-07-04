# users/permissions.py

from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'supervisor'

class IsBoy(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'boys'

class IsManagementStaff(BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['subadmin', 'supervisor', 'vice_supervisor']
        )
    
class IsSubadmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'subadmin'

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'supervisor'

class IsViceSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vice_supervisor'

class IsStaffRolesOnly(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            'subadmin', 'supervisor', 'vice_supervisor', 'boys'
        ]