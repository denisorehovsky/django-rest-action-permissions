class EvaluatePermissionsMixin:

    def has_permission(self, request, view):
        return self.evaluate_permissions('has_permission', request, view)

    def has_object_permission(self, request, view, obj):
        return self.evaluate_permissions(
            'has_object_permission', request, view, obj
        )
