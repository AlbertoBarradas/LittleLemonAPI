from rest_framework import permissions

class IsInManagerGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()