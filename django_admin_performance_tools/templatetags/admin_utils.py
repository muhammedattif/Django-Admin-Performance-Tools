# Django Imports
from django import template

register = template.Library()

# First Party Imports
from django_admin_performance_tools.quick_actions.registry import _registry


@register.simple_tag
def actions_list(request, name):
    """Get actions list for a site"""
    allowed_actions = []
    site_actions = _registry.get_site_actions(site_name=name)
    for action_class in site_actions:
        action = action_class(request=request)
        if action.has_permission():
            allowed_actions.append(action)
    return allowed_actions


@register.simple_tag
def build_admin_url(value):
    return "admin:%s" % (value)
