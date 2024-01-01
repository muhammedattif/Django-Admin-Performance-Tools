class SearchHelpTextMixin:
    """
    A mixin that dynamically set search_help_text based on search_fields
    """

    search_help_text_map = {}

    def get_changelist_instance(self, request):
        changelist = super().get_changelist_instance(request)
        changelist.search_help_text = self.get_search_help_text()
        return changelist

    def get_search_help_text(self) -> str:
        """Get search help text

        Returns:
            str: search help text
        """
        if self.search_help_text:
            return self.search_help_text

        return "Search is applied on the following: {0}".format(
            ", ".join(
                [
                    self.search_help_text_map.get(field, "") or field.replace("__", " ").replace("_", " ").title()
                    for field in self.search_fields
                ],
            ),
        )
