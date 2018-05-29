import abc
from six import with_metaclass
from .mixins import EvaluatePermissionsMixin


class BasePermission(with_metaclass(abc.ABCMeta)):
    """
    A base class from which all permission classes should inherit.
    """

    @abc.abstractmethod
    def has_permission(self, request, view):
        pass

    @abc.abstractmethod
    def has_object_permission(self, request, view, obj):
        pass


class BaseComponent(with_metaclass(abc.ABCMeta, BasePermission)):
    """
    A base class from which all component classes should inherit.
    """

    def __invert__(self):
        return Not(self)

    def __or__(self, component):
        return Or(self, component)

    def __and__(self, component):
        return And(self, component)


class Not(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, component):
        self.component = component

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return not getattr(self.component, permission_name)(*args, **kwargs)


class Or(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, *components):
        self.components = components

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return any(getattr(component, permission_name)(*args, **kwargs)
                   for component in self.components)


class And(EvaluatePermissionsMixin, BaseComponent):

    def __init__(self, *components):
        self.components = components

    def evaluate_permissions(self, permission_name, *args, **kwargs):
        return all(getattr(component, permission_name)(*args, **kwargs)
                   for component in self.components)
