# Python Standard Library Imports
from functools import wraps

# Django Imports
from django.contrib import messages


def check_queryset_max_selection_count(max_count):
    def _wrapper(func):
        def _wrapped_action(self, request, queryset):
            if queryset.count() > max_count:
                message = "Selection limit exceeded, selection limit is {0} instances".format(max_count)
                self.message_user(request, message, level=messages.ERROR)
                return
            return func(self, request, queryset)

        return _wrapped_action
    return _wrapper
