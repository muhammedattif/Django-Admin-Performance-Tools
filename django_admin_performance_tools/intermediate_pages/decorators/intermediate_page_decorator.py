# Django Imports
from django.http import HttpResponseRedirect
from django.shortcuts import render


def intermediate_page(
    form,
    template="admin/intermediate_pages/abstract_form_page.html",
    title=None,
    success_redirect_url=None,
):
    """a decorator function that generates an intermediate page for an action"""

    if not form.base_fields.get("_selected_action", None):
        raise ValueError(
            "An intermediate page's form must have the _selected_action field. Inherit from IntermediatePageForm to have it by default",
        )

    def _decorate(func):
        def _decorated_action(self, request, queryset, submitted_form=None):
            template_form = None
            action_func, action_name, template_title = self.get_action(func)

            if request.POST.get("apply", None):  # form submitted
                template_form = form(
                    request.POST,
                    request.FILES,
                    initial={"_selected_action": queryset.values_list("id", flat=True)},
                )
                if template_form.is_valid():
                    result = action_func(self=self, request=request, queryset=queryset, submitted_form=template_form)
                    if result is not False:
                        return HttpResponseRedirect(success_redirect_url or request.get_full_path())

            if template_form is None:  # has a form been submitted with errors?
                template_form = form(initial={"_selected_action": queryset.values_list("id", flat=True)})

            context = {
                "items": queryset,
                "form": template_form,
                "title": title or template_title.title(),
                "action_name": action_name,
                "opts": self.model._meta,
                **self.admin_site.each_context(request),
            }
            return render(request, template, context)

        return _decorated_action

    return _decorate
