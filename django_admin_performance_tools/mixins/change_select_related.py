# Django Imports
from django.core.checks import Error
from django.db.models.constants import LOOKUP_SEP

# First Party Imports
from django_admin_performance_tools.utils import get_0_depth_fields, get_related_fields


class ChangeSelectRelatedMixin:
    """
    Mixin to apply select related on change form fields
    """

    # Specify which level should we allow select related
    # min_change_select_related_depth = 1 means that selected fields must contains at least one LOOKUP_SEP
    # For example: min_change_select_related_depth = 1 allow ["field__related_field__..."] and does not allow ["field"]
    min_change_select_related_depth = 1
    change_select_related = []

    def get_change_select_related(self, form):
        """returns a list of related fields that will be selected"""
        return self.change_select_related

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.change_select_related:
            errors += self._validate_change_select_related_fields()
        return errors

    def _validate_change_select_related_fields(self):

        depth_0_fields = get_0_depth_fields(fields=self.change_select_related)
        related_fields = get_related_fields(model=self.model)

        invalid_realted_fields = set(depth_0_fields).difference(related_fields)
        if invalid_realted_fields:
            invalid_fields = ("'{0}'".format(s) for s in invalid_realted_fields)
            return [
                Error(
                    "Invalid field name(s) given in change_select_related: {0}. ".format(", ".join(invalid_fields)),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]

        invalid_depth_fields = list(
            filter(
                lambda field: len(field.split(LOOKUP_SEP)) - 1 < self.min_change_select_related_depth
                or len(field.split(LOOKUP_SEP)) - 1 > self.min_change_select_related_depth,
                self.change_select_related,
            ),
        )
        if invalid_depth_fields:
            invalid_fields = ("'{0}'".format(s) for s in invalid_depth_fields)
            return [
                Error(
                    "Invalid field name(s) given in change_select_related: {0}. "
                    "Minimum depth is: {1}".format(
                        ", ".join(invalid_fields),
                        self.min_change_select_related_depth,
                    ),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]
        return []

    def _apply_change_select_related(self, form):

        for related_field in self.get_change_select_related(form=form):
            splitted = related_field.split(LOOKUP_SEP)

            if len(splitted) > self.min_change_select_related_depth:
                field = splitted[0]
                if field not in form.base_fields:
                    continue
                related = LOOKUP_SEP.join(splitted[1:])
                form.base_fields[field].queryset = form.base_fields[field].queryset.select_related(related)


class AdminChangeSelectRelatedMixin(ChangeSelectRelatedMixin):
    """
    A mixin using change_select_related for change_form related fields

    NOTE: On overriding get_form method it must be decorated with @apply_change_select_related_on_admin_form
    """

    def apply_change_select_related_on_admin_form(func):
        """a decorator to be added on get_form() function"""

        def wrapper(self, *args, **kwargs):
            form = func(self, *args, **kwargs)
            self._apply_change_select_related(form)
            return form

        return wrapper

    @apply_change_select_related_on_admin_form
    def get_form(self, request, obj=None, change=False, **kwargs):
        return super(AdminChangeSelectRelatedMixin, self).get_form(request, obj, change, **kwargs)


class InlineChangeSelectRelatedMixin(ChangeSelectRelatedMixin):
    """
    Admin Inline using changes_select_related for get_formset related fields

    NOTE: On overriding get_formset method it must be decorated with @apply_change_select_related_on_inline_forms
    """

    def apply_change_select_related_on_inline_forms(func):
        """a decorator to be added on get_formset() function in inline"""

        def wrapper(self, *args, **kwargs):
            formset = func(self, *args, **kwargs)
            self._apply_change_select_related(formset.form)
            return formset

        return wrapper

    @apply_change_select_related_on_inline_forms
    def get_formset(self, request, obj=None, **kwargs):
        return super(InlineChangeSelectRelatedMixin, self).get_formset(request, obj, **kwargs)
