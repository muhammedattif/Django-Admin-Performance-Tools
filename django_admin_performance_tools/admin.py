from .mixins import (
    AdminChangeSelectRelatedMixin,
    InlineChangeSelectRelatedMixin,
    ListPrefetchRelatedMixin,
    NonSelectionActionsMixin,
    ReadonlySelectRelatedMixin,
    SearchHelpTextMixin,
)


class AbstractModelAdmin(
    ListPrefetchRelatedMixin,
    ReadonlySelectRelatedMixin,
    AdminChangeSelectRelatedMixin,
    SearchHelpTextMixin,
    NonSelectionActionsMixin,
):
    """
    Abstract model admin that is the entry point for all mixins
    """


class AbstractStackedInline(
    ReadonlySelectRelatedMixin,
    InlineChangeSelectRelatedMixin,
):
    """
    Abstract stacked inline admin that is the entry point for ReadonlySelectRelatedMixin/InlineChangeSelectRelatedMixin across all StackedInline admins
    """


class AbstractTabularInline(
    ReadonlySelectRelatedMixin,
    InlineChangeSelectRelatedMixin,
):
    """Abstract stacked inline admin that is the entry point for ReadonlySelectRelatedMixin/InlineChangeSelectRelatedMixin across all TabularInline admins"""
