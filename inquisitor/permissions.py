from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Deny access by default:
        allow_access = False

        # Check if one of the User's groups is the company group
        for group in request.user.groups.all():
            print(group.name)
            if group.name == obj.company_id:
                allow_access = True

        # Check if the user is a superuser
        if request.user.is_superuser:
            allow_access = True

        # Check if the user is part of ZD staff:
        if request.user.is_staff:
            allow_access = True

        return allow_access