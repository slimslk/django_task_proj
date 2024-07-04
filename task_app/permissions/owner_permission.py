from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAuthenticatedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        return obj.owner == request.user
