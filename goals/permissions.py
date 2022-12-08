from rest_framework.permissions import BasePermission


class UserAuthenticated(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
