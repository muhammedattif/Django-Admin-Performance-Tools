# Django Imports
from django.core.checks import Error

# First Party Imports
from django_admin_performance_tools.utils import get_0_depth_fields, get_related_fields, is_change_page


class ReadonlySelectRelatedMixin:
    """
    Mixin apply select related on readonly fields
    """

    readonly_select_related = []

    def get_readonly_select_related(self, request):
        """returns a list of readonly fields the will be selected"""
        return self.readonly_select_related

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.readonly_select_related:
            errors += self._validate_readonly_select_related_fields()
        return errors

    def _validate_readonly_select_related_fields(self):

        depth_0_fields = get_0_depth_fields(fields=self.readonly_select_related)
        related_fields = get_related_fields(model=self.model)

        invalid_realted_fields = set(depth_0_fields).difference(related_fields)
        if invalid_realted_fields:
            invalid_fields = ("'{0}'".format(s) for s in invalid_realted_fields)
            return [
                Error(
                    "Invalid field name(s) given in readonly_select_related: {0}. ".format(", ".join(invalid_fields)),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]

        # TODO: Use self.get_readonly_fields(request=request, obj=obj)
        invalid_readonly_fields = set(depth_0_fields).difference(self.readonly_fields)
        if invalid_readonly_fields:
            invalid_fields = ("'{0}'".format(s) for s in invalid_readonly_fields)
            return [
                Error(
                    "Invalid field name(s) given in readonly_select_related: {0}.".format(", ".join(invalid_fields)),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]

        return []

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if is_change_page(request=request) and self.get_readonly_select_related(request=request):
            queryset = self.apply_readonly_select_related(request=request, queryset=queryset)
        return queryset

    def apply_readonly_select_related(self, request, queryset):
        return queryset.select_related(*self.get_readonly_select_related(request=request))
