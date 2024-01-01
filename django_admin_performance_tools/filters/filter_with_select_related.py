# Django Imports

# Django Imports
from django.contrib import admin


class FilterWithSelectRelated(admin.RelatedFieldListFilter):
    list_select_related = []

    def field_choices(self, field, request, model_admin):
        return [(getattr(x, field.remote_field.get_related_field().attname), str(x)) for x in self.get_queryset(field)]

    def get_queryset(self, field):
        return field.remote_field.model._default_manager.select_related(*self.list_select_related)
