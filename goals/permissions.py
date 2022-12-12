from rest_framework.permissions import BasePermission, SAFE_METHODS

from goals.models.board import BoardParticipant


class UserAuthenticated(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True


class BoardPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()