from rest_framework import permissions
from .models import RolePermission

class RolePermissionRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        required_perm = getattr(view, 'required_permission', None)
        if required_perm is None:
            return True
        user_roles = request.user.userrole_set.all().values_list('role', flat=True)
        return RolePermission.objects.filter(role_id__in=user_roles, permission__name=required_perm).exists()