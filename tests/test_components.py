from rest_action_permissions.components import (
    AllowAny as TruePermissionComponent,
    DenyAll as FalsePermissionComponent
)


class TestActionPermissionComponent:

    def test_operator_or(self):
        assert (
            TruePermissionComponent() | TruePermissionComponent()
        ).has_permission(None, None)
        assert (
            TruePermissionComponent() | FalsePermissionComponent()
        ).has_permission(None, None)
        assert (
            FalsePermissionComponent() | TruePermissionComponent()
        ).has_permission(None, None)
        assert not (
            FalsePermissionComponent() | FalsePermissionComponent()
        ).has_permission(None, None)

    def test_operator_and(self):
        assert (
            TruePermissionComponent() & TruePermissionComponent()
        ).has_permission(None, None)
        assert not (
            TruePermissionComponent() & FalsePermissionComponent()
        ).has_permission(None, None)
        assert not (
            FalsePermissionComponent() & TruePermissionComponent()
        ).has_permission(None, None)
        assert not (
            FalsePermissionComponent() & FalsePermissionComponent()
        ).has_permission(None, None)

    def test_operator_not(self):
        assert not (~TruePermissionComponent()).has_permission(None, None)
        assert (~~TruePermissionComponent()).has_permission(None, None)
        assert (~FalsePermissionComponent()).has_permission(None, None)

    def test_chaining_operators(self):
        assert (
            TruePermissionComponent()
            & TruePermissionComponent()
            | FalsePermissionComponent()
        ).has_permission(None, None)
        assert (
            TruePermissionComponent() & ~FalsePermissionComponent()
        ).has_permission(None, None)
