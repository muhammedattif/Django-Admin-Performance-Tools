# Django Imports
from django.conf import settings

HIDE_QUICK_ACTIONS_DROPDOWN = getattr(settings, "HIDE_QUICK_ACTIONS_DROPDOWN", False)
HIDE_LANGUAGE_DROPDOWN = getattr(settings, "HIDE_LANGUAGE_DROPDOWN", False)
QUICK_ACTIONS_URL_PATH_PREFIX = getattr(settings, "QUICK_ACTIONS_URL_PATH_PREFIX", "quick-actions")
