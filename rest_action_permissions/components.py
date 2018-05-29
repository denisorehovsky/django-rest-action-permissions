from .base import BaseComponent


class ActionPermissionComponent(BaseComponent):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(ActionPermissionComponent):
    """
    Allow any access.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class DenyAll(ActionPermissionComponent):
    """
    Deny any access.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAuthenticated(ActionPermissionComponent):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminUser(ActionPermissionComponent):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUser(ActionPermissionComponent):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
