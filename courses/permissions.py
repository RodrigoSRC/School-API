from rest_framework import permissions
from rest_framework.views import View
from .models import Course


class AccountOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser

    def has_object_permission(self, request, view: View, obj: Course) -> bool:
        return request.user.is_superuser or request.user in obj.students.all()