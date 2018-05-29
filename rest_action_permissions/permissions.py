import inspect
import functools
import operator
from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions
from .base import BaseComponent, BasePermission
from .mixins import EvaluatePermissionsMixin


class ActionPermission(EvaluatePermissionsMixin, BasePermission):

    def evaluate_permissions(
        self, permission_name, request, view, *args, **kwargs
    ):
        perms = self._get_required_permissions(request, view)
        return getattr(perms, permission_name)(request, view, *args, **kwargs)

    def _get_required_permissions(self, request, view):
        action = self._get_action(view.action)
        action_perms_attr = '{}_perms'.format(action)
        perms = self._get_permissions_by_attr(action_perms_attr)
        if perms is None:
            if request.method in permissions.SAFE_METHODS:
                read_perms_attr = 'read_perms'
                perms = self._get_permissions_by_attr(read_perms_attr)
                if perms is None:
                    self._raise_attr_error(
                        general_attr=read_perms_attr,
                        action_attr=action_perms_attr
                    )
            else:
                write_perms_attr = 'write_perms'
                perms = self._get_permissions_by_attr(write_perms_attr)
                if perms is None:
                    self._raise_attr_error(
                        general_attr=write_perms_attr,
                        action_attr=action_perms_attr
                    )

        global_perms_attr = 'global_perms'
        global_perms = self._get_permissions_by_attr(global_perms_attr)
        if global_perms is not None:
            perms = global_perms & perms

        enough_perms_attr = 'enough_perms'
        enough_perms = self._get_permissions_by_attr(enough_perms_attr)
        if enough_perms is not None:
            perms = enough_perms | perms

        return perms

    def _get_permissions_by_attr(self, attr):
        if not hasattr(self, attr):
            return None
        perms = getattr(self, attr)
        perms = self._validate_permissions(
            perms=perms, attr=attr
        )
        return perms

    def _get_action(self, action):
        meta = getattr(self, 'Meta', None)
        partial_update_is_update = getattr(
            meta, 'partial_update_is_update', True
        )
        if action == 'partial_update' and partial_update_is_update:
            return 'update'
        return action

    def _validate_permissions(self, perms, attr):
        if isinstance(perms, BaseComponent):
            return perms
        elif isinstance(perms, (tuple, list)):
            validated_perms = (self._validate_permissions(perm, attr)
                               for perm in perms)
            # If we have a list of components, then we need to convert them
            # into one single component using `And` operator.
            return functools.reduce(operator.and_, validated_perms)
        elif inspect.isclass(perms) and issubclass(perms, BaseComponent):
            return perms()
        else:
            self._raise_validation_error(attr=attr)

    def _raise_attr_error(self, action_attr, general_attr):
        raise RuntimeError(
            '`{cls}` class must declare `{cls}.{action_attr}` or '
            '`{cls}.{general_attr}` attributes'.format(
                cls=self.__class__.__name__,
                action_attr=action_attr,
                general_attr=general_attr
            )
        )

    def _raise_validation_error(self, attr):
        raise ImproperlyConfigured(
            '`{cls}` class has invalid permission definition in '
            '`{cls}.{attr}` attribute'.format(
                cls=self.__class__.__name__,
                attr=attr
            )
        )
