# Django Imports
from django import forms


class IntermediatePageForm(forms.Form):
    """Abstract form with the needed data for an intermediate page form to work"""

    required_css_class = "required"

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
