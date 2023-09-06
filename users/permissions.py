from rest_framework import permissions


class IsSuperuserOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'me' in request.path.split('/'):
            return permissions.IsAuthenticated
        return request.user.is_superuser == 1
