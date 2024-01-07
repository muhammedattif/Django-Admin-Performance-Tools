# Python Standard Library Imports
from functools import reduce
from typing import List

# Django Imports
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.http.request import HttpRequest


def get_many_to_many_fields(model: models.Model) -> List[str]:
    """Get many to many fields of a model

    Args:
        model (models.Model): Model Class

    Returns:
        List[str]: A list of many to many fields
    """
    return [field.name for field in model._meta.get_fields() if field.many_to_many]


def get_related_fields(model: models.Model, include_many_to_many: bool = False) -> List[str]:
    """Get related fields of a model

    Args:
        model (models.Model): Model Class
        include_many_to_many (bool): Indicates that the returned fields includes ManyToMany Fields

    Returns:
        List[str]: A list of related fields
    """
    fields = [
        field.name for field in model._meta.get_fields() if (field.one_to_many or field.many_to_one or field.one_to_one)
    ]
    if include_many_to_many:
        fields += get_many_to_many_fields(model=model)
    return fields


def get_0_depth_fields(fields: List[str]) -> List[str]:
    """Get 0 depth names of fields based on LOOKUP_SEP seperator

    Args:
        fields (List[str]): list of fields that has 0 depth fields and more

    Returns:
        List[str]: splitted list that has only the first level of each field
    """

    return [field.split(LOOKUP_SEP)[0] for field in fields]


def is_change_page(request: HttpRequest) -> bool:
    """Check if the requested page is admin change

    Args:
        request (HttpRequest): HTTP Request

    Returns:
        bool: True if change, false if not
    """
    return request.resolver_match.view_name.endswith("change")


def is_changelist_page(request: HttpRequest) -> bool:
    """Check if the requested page is admin changelist

    Args:
        request (HttpRequest): HTTP Request

    Returns:
        bool: True if changelist, false if not
    """
    return request.resolver_match.view_name.endswith("changelist")


def join_slash(a, b):
    return a.rstrip("/") + "/" + b.lstrip("/")


def urljoin(*args):
    return reduce(join_slash, args) if args else ""
