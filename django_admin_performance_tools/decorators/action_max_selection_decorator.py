# Python Standard Library Imports
from inspect import isfunction

# Django Imports
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def check_queryset_max_selection(max_selection):
    if not isinstance(max_selection, int) and not isfunction(max_selection):
        raise TypeError("check_queryset_max_selection() argument: 'max_selection' must be an int or a callable")

    def _wrapper(func):
        def _wrapped_action(self, request, queryset):
            _max_selection = max_selection if isinstance(max_selection, int) else max_selection(request)
            if _max_selection > -1:
                if queryset.count() > _max_selection:
                    message = _("Selection limit exceeded, selection limit is {0} instance(s)").format(_max_selection)
                    self.message_user(request, message, level=messages.ERROR)
                    return
            return func(self, request, queryset)

        return _wrapped_action

    return _wrapper
