# Django Imports
from django.forms import widgets


class DisabledSelect(widgets.Select):
    option_template_name = "admin/forms/widgets/disabled_select_option.html"

    def __init__(self, attrs=None, disabled_options=[]):
        self.disabled_options = disabled_options
        super(DisabledSelect, self).__init__()

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["disabled_options"] = self.disabled_options
        return context
