from abc import ABC, abstractmethod


class Permission(ABC):
    """
    Permission abstraction.
    Child class should implement has_permission method.
    check_permission should always be called with kwargs.
    """

    @abstractmethod
    def check_permission(self, **kwargs):
        """
        Should raise ForbiddenError when not satisfied.
        """
        pass
