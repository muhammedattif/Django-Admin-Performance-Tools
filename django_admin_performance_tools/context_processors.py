# First Party Imports
from django_admin_performance_tools.settings import HIDE_LANGUAGE_DROPDOWN, HIDE_QUICK_ACTIONS_DROPDOWN


def settings(request):
    return {
        "is_language_dropdown_visible": not HIDE_LANGUAGE_DROPDOWN,
        "is_quick_actions_dropdown_visible": not HIDE_QUICK_ACTIONS_DROPDOWN,
    }
