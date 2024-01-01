# Django Admin Performance Tools

[![python](https://img.shields.io/badge/Python-v3.8-3776AB.svg?style=flat&logo=python&logoColor=yellow)](https://www.python.org)  [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Table of Contents

- [Description](#1--description)
- [Requirements](#2--requirements)
- [Installation Instructions](#3--installation-instructions)
- [Quick Actions](#4--quick-actions)
- [Languages Dropdown](#5--languages-dropdown)
- [Intermediate Pages and Model Action Tools](#6--intermediate-pages-and-model-action-tools)
- [Tools for admin Querysets/Filters](#7--tools-for-admin-querysets-and-filters-optemization)
- [Tools for admin search/filters](#8--tools-for-admin-search-and-filters)
- [Settings](#9--Settings)

# 1- Description

This Package is a collection of extensions/tools for the default django administration interface, it includes:
-   Quick Actions
-   Languages Dropdown Interface
-   Intermediate Pages and model actions tools
-   Tools for admin `Querysets`/`Filters` optemization (helps avoiding N+1 issue)
-   Tools for admin `search`/`filters`
-   Widgets

---

**Full documentation is avilable on [Github Repo][github-repo]**

# 2- Requirements
Before you begin, ensure you have met the following requirements:
* Python 3.8+
* Django >= 3.2 

---

# 3- Installation Instructions

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```bash
pip install django-admin-performance-tools
```

Add 'django_admin_performance_tools' to your INSTALLED_APPS settings.
```python
INSTALLED_APPS = [
    "django_admin_performance_tools",
    ...
]
```
**Must be added on the top of the list**

---

# 4- Quick Actions

Quick Actions is a new feature that allows you to take actions quickly from the admin home page, it is the same as actions in the model admin page, but the main differences are:
-   It is not attached to any model
-   Actions acts like views and support all http methods (`POST`, `GET`, `PUT`, `DELETE`)
-   Support permissions, so you can write your own logic to control who can see the action
-   Form View Action is introduced to enables you to create an action to render any form (It is implemented on top of django FormView)

**Setup**

in `settings.py` replace `django.contrib.admin` by `django_admin_performance_tools.sites.MainAdminConfig` in your INSTALLED_APPS.
```python
INSTALLED_APPS = [
    "django_admin_performance_tools",
    "django_admin_performance_tools.sites.MainAdminConfig",
    ...
]
```

in `settings.py` update TEMPLATES
```python

TEMPLATES = [
    {
        ...
        'DIRS': ["templates"]
    },
]
```

in `settings.py` update TEMPLATES
```python

TEMPLATES = [
    {
        ...
        'DIRS': ["templates"]
        'OPTIONS': {
            'context_processors': [
                ...
                "django_admin_performance_tools.context_processors.settings",
            ],
        },
    },
]
```

![Alt text](/docs/images/quick_actions_dropdown.gif?raw=true "Quick Actions Dropdown")

## 4.1- FormViewQuickAction

Form View Quick Action is used to create an action to render a form (It is implemented on top of django FormView) 

**Example:**

```python
from django_admin_performance_tools.quick_actions import FormViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class FormAction(FormViewQuickAction):
    name = "My Form Action"
    form_class = MyForm
```

-To customize submit button name, you can set `submit_button_value` attribute in the `FormAction` class

-To customize success redirection of the form you can set `success_url` attribute or override `get_success_url` function.
 

## 4.2- TemplateViewQuickAction

Template View Quick Action is used to create an action to render a template (It is implemented on top of django TemplateView) 

**Example:**

```python
from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class TemplateAction(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"
```

**Notes**

-The template file you created (`my_template.html`) must extends from `base_quick_action.html`

```bash
{% extends 'admin/quick_actions/base_quick_action.html' %}
```

## 4.3- Abstract QuickAction

QuickAction is used to create a custom action, that means you will've to implement `get()`, `post()`, `put()`, or `delete()` yourself (It is implemented on top of django View) 

**Example:**

```python
from django_admin_performance_tools.quick_actions import QuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class CustomAction(QuickAction):
    name = "My custom Action"

    def get(self, request, *args, **kwargs):
        # Write your own logic here
    
    def post(self, request, *args, **kwargs):
        # Write your own logic here

    def put(self, request, *args, **kwargs):
        # Write your own logic here

    def delete(self, request, *args, **kwargs):
        # Write your own logic here
    
    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        return {
            # Pass your extra context here
            **super().get_context_data(**kwargs),
        }
```

You can override `get_context_data()` function to pass extra context values on creating a custom actions


## 4.4- Control who can see the actions

You can override `has_permission()` function to control who can see the actions

**Example:**

```python
from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class TemplateAction(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"

    def has_permission(self):
        # Write your own logic here
        return super().has_permission()
```

Quck actions by default check the `is_active=True` and `is_staff=True` thats why you must call `super().has_permission()` on overriding `has_permission()` function.

---
**Notes**

1- **All actions must be added/imported in admin.py as to be detected and registered.**

---

## 5- Languages Dropdown

This will show a dropdown menu in the admin pages that allows you change the site language easily, so all you have to do is to add the following URLs in the main root `urls.py` file

**Setup**

in the root `urls.py` add the following: 

```python
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    ...
]
```
Add 'django_admin_performance_tools' to your INSTALLED_APPS setting.
in `settings.py` add `django.middleware.locale.LocaleMiddleware` to the MIDDLEWARE

```python
MIDDLEWARE = [
    ...
    "django.middleware.locale.LocaleMiddleware",
]
```

And that is it

![Alt text](/docs/images/languages_dropdown.png?raw=true "Languages Dropdown")



---

# 6- Intermediate Pages and Model Action Tools

## 6.1- Intermediate Pages

We introduce `Intermediate Pages` for admin actions to render a form before proceeding to the action logic. This will help if you need to pass extra params to your actions.

**Example:**

```python
from django import forms
from django.contrib import admin
from django.contrin.auth.models import User

from django_admin_performance_tools.intermediate_pages.decorators import intermediate_page
from django_admin_performance_tools.intermediate_pages.forms import IntermediatePageForm

from .models import MyModel

class MyForm(IntermediatePageForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    
    actions = ["assign_user"]
    
    @intermediate_page(form=MyForm)
    def assign_user(self, request, queryset):
        user = request.data.get("user")
        # Write your own Logic
```

Intermediate Pages forms can be imported from :
```python
from django_admin_performance_tools.intermediate_pages.forms import IntermediatePageForm, IntermediatePageModelForm
```

-**IntermediatePageForm** is implemented on top of `forms.Form`

-**IntermediatePageModelForm** is implemented on top of `forms.ModelForm`

## 6.2- Non-Selection Actions

The existing Django actions require at least one selected instance to proceed, so
We introduce `Non-Selection Actions` for admin actions to proceed to the action without selecting any instances.


**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.mixins import NonSelectionActionsMixin

from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(NonSelectionActionsMixin, admin.ModelAdmin):
    
    actions = ["assign_user"]
    non_selection_actions = ["assign_user"]

    def assign_user(self, request, queryset):
        # Write your own Logic
```

## 6.3- Max Selection Count

The existing Django actions allows all staff users to select all the queryset and apply the action on it, imagine you have a 1 Million records and a staff user selected all the queryset and applied the action on it! 

So ,We introduced `Max Selection Count` to set max instances to be selected to an action.

**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.decorators import check_queryset_max_selection_count

from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    
    actions = ["assign_user"]

    @check_queryset_max_selection_count(max_count=100)
    def assign_user(self, request, queryset):
        # Write your own Logic
```
----

# 7- Tools for admin Querysets and Filters optemization

## 7.1- Readonly Select Related

All `ModelAdmin`/`StackedInline`/`TabularInline` hits the db to fetch all related fields in `readonly_fields` list


**Example:**

```python
from django.contrib import admin
from .models import MyModel, AnotherModel

class MyModel(models.Model):

    related_field_1 = models.ForeignKey(...)
    related_field_2 = models.ForeignKey(...)
    related_field_3 = models.ForeignKey(...)
    related_field_4 = models.ForeignKey(...)


class AnotherModel(models.Model):

    my_model = models.ForeignKey(MyModel)
    related_field_5 = models.ForeignKey(...)
    related_field_6 = models.ForeignKey(...)
    related_field_7 = models.ForeignKey(...)

class AnotherModelInline(admin.StackedInline):
    model = AnotherModel
    readonly_fields = [
        "related_field_5",
        "related_field_6",
        "related_field_7"
    ]


@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    inlines = [AnotherModelInline]
    redaonly_fields = [
        "related_field_1",
        "related_field_2",
        "related_field_3",
        "related_field_4"
    ]

```

Consider the above example Django will hit the DB 7 times to get the related fields and this number will increase if more inlines are added.

So, We introduce `readonly_select_related` to select all read-only fields while rendering the models and its inlines

**Example:**

```python
from django.contrib import admin
from django_admin_performance_tools.mixins import ReadonlySelectRelatedMixin
from .models import MyModel, AnotherModel

class MyModel(models.Model):

    related_field_1 = models.ForeignKey(...)
    related_field_2 = models.ForeignKey(...)
    related_field_3 = models.ForeignKey(...)
    related_field_4 = models.ForeignKey(...)


class AnotherModel(models.Model):

    my_model = models.ForeignKey(MyModel)
    related_field_5 = models.ForeignKey(...)
    related_field_6 = models.ForeignKey(...)
    related_field_7 = models.ForeignKey(...)

class AnotherModelInline(ReadonlySelectRelatedMixin, admin.StackedInline):
    model = AnotherModel
    readonly_fields = [
        "related_field_5",
        "related_field_6",
        "related_field_7"
    ]
    readonly_select_related = [
        "related_field_5",
        "related_field_6",
        "related_field_7"
    ]


@admin.register(MyModel)
class MyModelAdmin(ReadonlySelectRelatedMixin, admin.ModelAdmin):
    
    inlines = [AnotherModelInline]
    redaonly_fields = [
        "related_field_1",
        "related_field_2",
        "related_field_3",
        "related_field_4"
    ]
    readonly_select_related = [
        "related_field_1",
        "related_field_2",
        "related_field_3",
        "related_field_4"
    ]
```


## 7.2- List Prefetch Related

Django `list_display` allows functions that are decorated by `@admin.display`, in these functions you may access a reverse relation or many-to-many fields of the instance, this means that the admin will hit the DB in every row to get the data and this will lead to a huge number of queries and may cause N+1 issue

**Example:**

```python
from django.contrib import admin
from django.contrin.auth.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = [
        "name",
        "email,
        "groups
    ]

    @admin.display
    def groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return " ".join(groups)

```

Consider that the page loaded 100 users the above example will hit the DB 100 times to get the related groups of each user.

So, We introduce `list_prefetch_related` to prefetch all reverse relations while rendering the changelist page
**Example:**

```python
from django.contrib import admin
from django.contrin.auth.models import User
from django_admin_performance_tools.mixins import ListPrefetchRelatedMixin

@admin.register(User)
class UserAdmin(ListPrefetchRelatedMixin, admin.ModelAdmin):
    
    list_display = [
        "name",
        "email,
        "groups
    ]
    list_prefetch_related = ["groups"]

    @admin.display
    def groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return " ".join(groups)
```


## 7.3- Change Prefetch Related

Default behavior of Django admin is to render all the related fields of an instance in dropdowns and call model's `__str__` function for each row in this dropdowns


**Example:**

```python
from django.contrib import admin
from django.contrin.auth.models import User
from .models import MyModel, AnotherModel


class AnotherModel(models.Model):

    name = models.CharField()
    user = models.ForeignKey(User)
    
    def __str__(self):
        return f"{self.name} User: {self.user.username}"


class MyModel(models.Model):

    name = models.CharField()
    another_model = models.ForeignKey(AnotherModel)

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    
    fields = [
        "name",
        "another_model"
    ]
```

Consider the above example, a form will be rendered with two fields `name` and `another_model` imagine that `another_model` dropdown has 100 row, and `__str__ ` function of `AnotherModel` access the user to get its username, this means that in every row Django will hit the DB to fetch the username of the user.

So, We introduce `change_select_related` to select all related fields while rendering the change page
**Example:**

```python
from django.contrib import admin
from django.contrin.auth.models import User
from django_admin_performance_tools.mixins import AdminChangeSelectRelatedMixin
from .models import MyModel, AnotherModel


class AnotherModel(models.Model):

    name = models.CharField()
    user = models.ForeignKey(User)
    
    def __str__(self):
        return f"{self.name} User: {self.user.username}"


class MyModel(models.Model):

    name = models.CharField()
    another_model = models.ForeignKey(AnotherModel)

@admin.register(MyModel)
class MyModelAdmin(AdminChangeSelectRelatedMixin, admin.ModelAdmin):
    
    fields = [
        "name",
        "another_model"
    ]
    change_select_related = ["another_model__user"]
```

It is supported in inlines too

**Example:**

```python
from django_admin_performance_tools.mixins import InlineChangeSelectRelatedMixin
from .models import AnotherModel

class AnotherModelInline(InlineChangeSelectRelatedMixin, admin.StackedInline):
    model = AnotherModel
    change_select_related = [...]
```

# 8- Tools for admin search and filters

## 8.1 Search Help Text

Recently Django featured a new admin attribute `search_help_text` and it adds a help text below the search bar, So we extended this feature to be more useful and readable by showing all the fields that the admin will search in.

![Alt text](/docs/images/search_help_text.png?raw=true "Languages Dropdown")

**Example:**

```python

from django.contrib import admin
from django.contrin.auth.models import User
from django_admin_performance_tools.mixins import SearchHelpTextMixin

@admin.register(User)
class UserAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    
    search_fields = [
        "email",
        "name",
        "username",
        "phone_number"
    ]

```

Not just field names, you can customize any field to represent another text

**Example:**

```python

from django.contrib import admin
from django.contrin.auth.models import User
from django_admin_performance_tools.mixins import SearchHelpTextMixin

@admin.register(User)
class UserAdmin(SearchHelpTextMixin, admin.ModelAdmin):
    
    search_fields = [
        "email",
        "name",
        "username",
        "phone_number"
    ]
    search_help_text_map = {
        "email": "Email Address"
    }
```


There is an abstract class to use if you intend to use all the following features in Model Admin:

- ListPrefetchRelatedMixin
- ReadonlySelectRelatedMixin
- AdminChangeSelectRelatedMixin
- SearchHelpTextMixin
- NonSelectionActionsMixin

can be imported from the following path:

```python
from django_admin_performance_tools.admin import AbstractModelAdmin
```

There is an abstract classes to use if you intend to use all the following features in Inline Admin:

- ReadonlySelectRelatedMixin
- AdminChangeSelectRelatedMixin

can be imported from the following path:

```python
from django_admin_performance_tools.admin import (
    AbstractStackedInline, 
    AbstractTabularInline
)
```

# 9- Settings

You can controll some behaves by adding the following in `settings.py`

**- HIDE_QUICK_ACTIONS_DROPDOWN**

This will hide the Quick Actions dropdown from admin sites

Default value is `False`

**- HIDE_LANGUAGE_DROPDOWN**

This will hide the Languages dropdown from admin sites

Default value is `False`


[github-repo]: https://github.com/muhammedattif/Django-Admin-Performance-Tools