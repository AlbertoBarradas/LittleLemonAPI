from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsInManagerGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()
    
class IsManagerOrSuperAdmin(BasePermission):
    def has_permission(self,request, view):
        user = request.user
        return(
            user and user.is_authenticated and (user.is_superuser or user.groups.filter(name="Manager").exists())
        )