# Python Standard Library Imports
from functools import update_wrapper

# Django Imports
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.urls import path


class AbstractAdminSiteMixin:
    """AbstractAdminSite"""

    def each_context(self, request):
        context = super().each_context(request)
        context["name"] = self.name
        return context

    def get_urls(self):

        # First Party Imports
        from django_admin_performance_tools.quick_actions.registry import _registry

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(admin_site=self, *args, **kwargs)

            return update_wrapper(wrapper, view)

        extra_urls = []
        for action in _registry.get_site_actions(site_name=self.name):
            extra_urls.append(
                path(
                    action.get_url_path(),
                    wrap(action.as_view()),
                    name=action.get_path_name(),
                ),
            )

        return extra_urls + super().get_urls()


class MainAdminConfig(AdminConfig):
    default_site = "django_admin_performance_tools.sites.MainAdmin"


class MainAdmin(AbstractAdminSiteMixin, AdminSite):
    """Main Admin Site"""
