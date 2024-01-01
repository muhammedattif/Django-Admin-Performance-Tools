# Other Third Party Imports
from admin_auto_filters.filters import AutocompleteFilter as ACF


def AutocompleteFilter(title: str, field: str) -> ACF:
    _title = title

    class ACFilter(ACF):
        title = _title
        field_name = field

    return ACFilter
