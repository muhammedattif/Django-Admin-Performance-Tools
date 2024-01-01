# Python Standard Library Imports
import itertools

# Django Imports
from django.core.exceptions import ImproperlyConfigured

# First Party Imports
from django_admin_performance_tools.settings import HIDE_QUICK_ACTIONS_DROPDOWN

from .base_actions import BaseAction

NON_SITE = "_non_site"


class Registry:
    """Registry class which is responsible for registering actions dynamically"""

    sites_actions = {
        NON_SITE: [],
    }

    def register(self, action_class, sites=[]):
        if not sites:
            if any(action_class.__name__ == action.__name__ for action in self.sites_actions[NON_SITE]):
                raise ImproperlyConfigured(
                    "{0} Already Resistered".format(action_class.__name__),
                )
            self.sites_actions[NON_SITE].append(action_class)
        else:
            for site in sites:
                if any(
                    action_class.__name__ == action.__name__ for action in self.get_site_actions(site_name=site.name)
                ):
                    raise ImproperlyConfigured(
                        "{0} Already Resistered in {1}".format(action_class.__name__, site.__class__.__name__),
                    )
                self.sites_actions.setdefault(site.name, []).append(action_class)

    @property
    def actions(self):
        return list(itertools.chain.from_iterable(self.sites_actions.values()))

    def get_site_actions(self, site_name):
        site_actions = self.sites_actions.get(site_name, [])
        non_site_actions = self.sites_actions.get(NON_SITE, [])
        return site_actions + non_site_actions


def register_quick_action(sites=[]):
    """
    Register the given action

    Usage:

    @register_quick_action(sites=[Site1, Site2])
    class CustomQuickAction(QuickAction):
        pass

    """

    def _action_wrapper(action_class):
        if not issubclass(action_class, BaseAction):
            raise ImproperlyConfigured("{0} Class must subclass BaseAction".format(action_class.__name__))

        if not HIDE_QUICK_ACTIONS_DROPDOWN:
            _registry.register(action_class=action_class, sites=sites)
        return action_class

    return _action_wrapper


_registry = Registry()
