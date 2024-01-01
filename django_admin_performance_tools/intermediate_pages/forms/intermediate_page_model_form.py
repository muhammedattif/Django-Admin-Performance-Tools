# Django Imports
from django import forms

from .intermediate_page_form import IntermediatePageForm


class IntermediatePageModelForm(IntermediatePageForm, forms.ModelForm):
    """Abstract model form with the needed data for an intermediate page form to work"""
