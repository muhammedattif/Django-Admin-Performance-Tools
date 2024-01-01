# Django Imports
from django.core.checks import Error

# First Party Imports
from django_admin_performance_tools.utils import get_0_depth_fields, get_many_to_many_fields, is_changelist_page


class ListPrefetchRelatedMixin:
    """
    Mixin to apply prefetch related on admin list display fields
    """

    list_prefetch_related = []

    def get_list_prefetch_related(self, request):
        """returns a list of fields the will be prefetched"""
        return self.list_prefetch_related

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.list_prefetch_related:
            errors += self._validate_list_prefetch_related_fields()
        return errors

    def _validate_list_prefetch_related_fields(self):

        depth_0_fields = get_0_depth_fields(fields=self.list_prefetch_related)
        related_fields = get_many_to_many_fields(model=self.model)

        invalid_realted_fields = set(depth_0_fields).difference(related_fields)
        if invalid_realted_fields:
            invalid_fields = ("'{0}'".format(s) for s in invalid_realted_fields)
            return [
                Error(
                    "Invalid field name(s) given in list_prefetch_related: {0}. ".format(", ".join(invalid_fields)),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]
        return []

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if is_changelist_page(request=request) and self.get_list_prefetch_related(request=request):
            queryset = self.apply_list_prefetch_related(request=request, queryset=queryset)
        return queryset

    def apply_list_prefetch_related(self, request, queryset):
        return queryset.prefetch_related(*self.get_list_prefetch_related(request=request))
