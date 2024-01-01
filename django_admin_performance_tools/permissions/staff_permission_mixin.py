# Django Imports
from django.contrib.auth.mixins import PermissionRequiredMixin


class StafUserPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        if self.request.user.is_active and self.request.user.is_staff:
            return True
        return False
