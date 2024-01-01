# Python Standard Library Imports
from re import sub

# Django Imports
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

# First Party Imports
from django_admin_performance_tools.permissions import StafUserPermissionRequiredMixin


class BaseAction(StafUserPermissionRequiredMixin):
    """A Base action class to be inherited when initializing a custom action"""

    name = None
    url_path = None
    path_name = None

    def get_context_data(self, **kwargs):
        admin_site = self.kwargs["admin_site"]
        return {
            "action": self,
            **super().get_context_data(**kwargs),
            **admin_site.each_context(self.request),
        }

    @classmethod
    def get_name(cls):
        if cls.name:
            return cls.name
        name = sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(cls.__name__))
        cls.name = name.replace("action", "").replace("Action", "").strip()
        return cls.name

    @classmethod
    def get_url_path(cls):
        if cls.url_path:
            return cls.url_path
        name = sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(cls.__name__))
        cls.url_path = name.lower().replace(" ", "-")
        return cls.url_path

    @classmethod
    def get_path_name(cls):
        if cls.path_name:
            return cls.path_name
        cls.path_name = cls.get_url_path()
        return cls.path_name


class QuickAction(BaseAction, View):
    """An abstract action class to be inherited when creating custom actions"""


class TemplateViewQuickAction(BaseAction, TemplateView):
    """An action class to be inherited when initializing an action to render a template"""
    
    
class AbstractFormViewQuickAction(BaseAction):
    """An abstract class for form actions"""

    submit_button_value = "Go"
    success_url = None
    
    def get_success_url(self) -> str:
        if self.success_url:
            return self.success_url
        return reverse_lazy("admin:{0}".format(self.path_name))
    
    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        return {
            "submit_button_value": self.__class__.submit_button_value,
            **super().get_context_data(**kwargs),
        }

class FormViewQuickAction(AbstractFormViewQuickAction, FormView):
    """An action class to be inherited when initializing an action to render a form"""

    template_name = "admin/quick_actions/form_view_quick_action.html"


class WizardFormViewQuickAction(AbstractFormViewQuickAction):
    """An action class to be inherited when initializing an action to render a wizard forms"""
    template_name = "admin/quick_actions/wizard_form_view_quick_action.html"
    
    def done(self, form_list, **kwargs):
        return redirect(self.get_success_url())