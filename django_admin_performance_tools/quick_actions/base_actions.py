# Python Standard Library Imports
from re import sub

# Django Imports
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, FormView

# First Party Imports
from django_admin_performance_tools.permissions import StafUserPermissionRequiredMixin


class BaseAction(StafUserPermissionRequiredMixin):
    """A Base action class to be inherited when initializing a custom action"""

    name = None
    url_path = None
    path_name = None
    post_success_message = None

    def post(self, request, bypass_success_message=False, *args, **kwargs):
        success_message = self.get_post_success_message()
        if success_message and not bypass_success_message:
            messages.success(request=request, message=success_message)
        return super().post(request, *args, **kwargs)

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

    def get_post_success_message(self):
        return self.post_success_message


class QuickAction(BaseAction, View):
    """An abstract action class to be inherited when creating custom actions"""


class TemplateViewQuickAction(BaseAction, TemplateView):
    """An action class to be inherited when initializing an action to render a template"""


class AbstractFormViewQuickAction(BaseAction):
    """An abstract class for form actions"""

    template_name = "admin/quick_actions/form_view_quick_action.html"
    submit_button_value = _("Go")
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


class CreateViewQuickAction(AbstractFormViewQuickAction, CreateView):
    """An action class to be inherited when initializing an action to render a model form to craete an instance"""

    submit_button_value = _("Create")


class WizardFormViewQuickAction(AbstractFormViewQuickAction):
    """An action class to be inherited when initializing an action to render a wizard forms"""

    template_name = "admin/quick_actions/wizard_form_view_quick_action.html"

    def post(self, request, *args, **kwargs):
        bypass_success_message = self.steps.current != self.steps.last
        return super().post(request=request, bypass_success_message=bypass_success_message, *args, **kwargs)

    def done(self, form_list, **kwargs):
        return redirect(self.get_success_url())
