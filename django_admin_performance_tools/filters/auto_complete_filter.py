def AutocompleteFilter(title: str, field: str):
    _title = title
    
    # Other Third Party Imports
    from admin_auto_filters.filters import AutocompleteFilter as ACF
    class ACFilter(ACF):
        title = _title
        field_name = field

    return ACFilter
