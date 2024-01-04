# Django Imports
from django.contrib.admin.views.main import ChangeList
from django.core.checks import Error
from django.core.handlers.wsgi import WSGIRequest


class NoSelectionActionsChangeListMixin:
    """A mixin for Non-Selection Actions Change list Class"""

    def get_results(self, request: WSGIRequest) -> None:
        super().get_results(request)
        self.show_admin_actions = True


class NoSelectionActionsChangeList(NoSelectionActionsChangeListMixin, ChangeList):
    """Non-Selection Actions Change list class"""


class NonSelectionActionsMixin:
    """
    Mixin to apply non selection actions, Actions will be submitted without selecting any instences
    """

    non_selection_actions = []

    def get_non_selection_actions(self, request):
        """returns a list of actions that do not need a selection from queryset"""
        return self.non_selection_actions

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.non_selection_actions:
            errors += self._validate_non_selection_actions()
        return errors

    def _validate_non_selection_actions(self):
        invalid_actions = set(self.non_selection_actions).difference(self.actions)
        if invalid_actions:
            return [
                Error(
                    "Following non selection action(s) {0} must be added to {1}.actions".format(
                        ", ".join(invalid_actions),
                        self.__class__.__name__,
                    ),
                    obj=self.__class__,
                    id="admin.E130",
                ),
            ]
        return []

    def changelist_view(self, request, extra_context=None):
        if "action" in request.POST and request.POST["action"] in self.get_non_selection_actions(request):
            selected_action = request.POST.getlist("_selected_action")
            if not selected_action or selected_action[0] == "":
                post = request.POST.copy()
                post.setlist("_selected_action", [None])
                request._set_post(post)
        return super().changelist_view(request, extra_context)

    def get_changelist(self, request, **kwargs):
        """
        Return the ChangeList class for use on the changelist page.
        """
        if self.non_selection_actions:
            return NoSelectionActionsChangeList
        return ChangeList

    def get_action_choices(self, request, **kwargs):
        action_choices = super().get_action_choices(request, **kwargs)
        if self.non_selection_actions and not self.get_queryset(request).count():
            return filter(lambda action_choice: action_choice[0] in self.non_selection_actions, action_choices)
        return action_choices
