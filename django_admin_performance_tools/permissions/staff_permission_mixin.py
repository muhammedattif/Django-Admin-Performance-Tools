# Django Imports
from django.contrib.auth.mixins import PermissionRequiredMixin


class StafUserPermissionRequiredMixin(PermissionRequiredMixin):
    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            perms = []
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required

        return perms

    def has_permission(self):
        perms = self.get_permission_required()
        if perms:
            permitted = self.request.user.has_perms(perms)
            if not permitted:
                return False
        # NOTE: This check is already done by the admin site level, but we double check it here
        if not (self.request.user.is_active and self.request.user.is_staff):
            return False
        return True
