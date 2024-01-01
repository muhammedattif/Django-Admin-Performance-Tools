# Django Imports
from django.contrib import admin


class CustomTitledChoicesFieldListFilter(admin.ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = f"{field.model._meta.verbose_name} {field.name.title()} "
