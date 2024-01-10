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
- [Widgets](#9--widgets)
- [Settings](#10--Settings)

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


in `settings.py` update TEMPLATES
```python

TEMPLATES = [
    {
        ...
        'DIRS': ["templates"],
        'OPTIONS': {
            'context_processors': [
                ...
                "django_admin_performance_tools.context_processors.settings",
            ],
        },
    },
]
```

---

# 4- Quick Actions

Quick Actions is a new feature that allows you to take actions quickly from the admin home page, it is the same as actions in the model admin page, but the main differences are:
-   It is not attached to any model
-   Actions acts like views but only supports (`POST`, `GET`) http methods
-   Support permissions, so you can write your own logic to control who can see the action
-   Form View Action is introduced to enables you to create an action to render any form (It is implemented on top of django FormView and CreateView)
-   Wizard Form View Action is introduced to enables you to create multi-step forms (It is implemented on top of django-formtools)
-   Template View Action is introduced to enables you to render your own templates
-   Base View Action is introduced to enables you to create customized actions as you want

**Setup**

in `settings.py` replace `django.contrib.admin` by `django_admin_performance_tools.sites.MainAdminConfig` in your INSTALLED_APPS.
```python
INSTALLED_APPS = [
    "django_admin_performance_tools",
    "django_admin_performance_tools.sites.MainAdminConfig",
    ...
]
```


![Alt text](/docs/images/quick_actions_dropdown.gif?raw=true "Quick Actions Dropdown")
🚀🚀

What if you already implemented your own Admin site? all you've to do is to inherit from `AbstractAdminSiteMixin`

**Example:**

```python
from django_admin_performance_tools.sites import AbstractAdminSiteMixin


class YourAdmin(AbstractAdminSiteMixin, AdminSite):
    """Your Admin Site"""
```
by doing that you don't need to replace your admin site in `INSTALLED_APPS`

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

    def post(self, request, *args, **kwargs):
        # Write your logic here
        return super().post(request, *args, **kwargs)

```

-To customize submit button name, you can set `submit_button_value` attribute in the `FormAction` class

-To customize success redirection of the form you can set `success_url` attribute or override `get_success_url` function (Default is redirect to the action page).


## 4.2- CreateViewQuickAction

Create View Quick Action is used to create an action to render a model form (It is implemented on top of django CreateView)

**Example:**

```python
from django_admin_performance_tools.quick_actions import CreateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

from .models import MyModel

@register_quick_action()
class CreateFormAction(CreateViewQuickAction):
    name = "My Craete Form Action"
    model = model
    fields = ["name"]
```

-To customize submit button name, you can set `submit_button_value` attribute in the `CreateFormAction` class

-To customize success redirection of the form you can set `success_url` attribute or override `get_success_url` function (Default is redirect to the action page).


## 4.3- WizardFormViewQuickAction

Wizard Form View Quick Action is implemented on top of [django-formtools][django-formtools] library, and it is used to create an action to render a wizard form.

**setup**

`django-formtools` library is required. to install it use the following pip command:

```bash
pip install django-formtools
```

Add 'formtools' to your INSTALLED_APPS settings.
```python
INSTALLED_APPS = [
    ...
    "formtools",
]
```

**Example:**

```python
from formtools.wizard.views import SessionWizardView

from django_admin_performance_tools.quick_actions import WizardFormViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class WizardFormAction(WizardFormViewQuickAction, SessionWizardView):
    name = "My Wizard Form Action"
    form_list = [Form1, Form2, Form3]

    def done(self, form_list, **kwargs):
        # form_list[0].cleaned_data
        # form_list[1].cleaned_data
        # form_list[2].cleaned_data
        # Continue writing your logic here
        return super().done(form_list, **kwargs)
```

And that's it 🎉

![Alt text](/docs/images/wizard_actions.gif?raw=true "Wizard Actions")

-To customize last step button name, you can set `submit_button_value` attribute in the `WizardFormAction` class

-To customize `done()` function redirection you can set `success_url` attribute or override `get_success_url` function (Default is redirect to the action page).

## 4.4- TemplateViewQuickAction

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

{% block action_body %}
    # Write your own HTML
{% endblock %}
```

## 4.5- Abstract QuickAction

QuickAction is used to create a custom action, that means you will've to implement `get()`, `post()` yourself (It is implemented on top of django View)

**Example:**

```python
from django_admin_performance_tools.quick_actions import QuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class CustomAction(QuickAction):
    name = "My custom Action"

    def get(self, request, *args, **kwargs):
        # Write your own logic here
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Write your own logic here
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        return {
            # Pass your extra context here
            **super().get_context_data(**kwargs),
        }
```

You can override `get_context_data()` function to pass extra context values


## 4.6- Control who can see the actions

Quick actions acts like views so you can set `permission_required` attribute or override `get_permission_required()`, `has_permission()` methods to control who can see the actions.

**Example:**

```python
from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action

@register_quick_action()
class TemplateAction(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"
    permission_required = ("myapp.add_mymodel")

    def has_permission(self):
        # Write your own logic here
        return super().has_permission()
```
the previous example will check the following by default:
- The user has add permission on MyModel View
- The user is active and is staff


**Notes**

- On overriding `has_permission()` you must call `super()`. Default check the user `is_active=True` and `is_staff=True`
- `permission_required` attribute default value is `None`

## 4.7- Register Quick Actions to Multiple Admin Sites

`@register_quick_action()` decorator register the action to all admin sites, so if you need to register an action to a specific site you can pass `sites=[site1, site2, site3]` to the decorator

**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action
from .my_sites import site2, site3

@register_quick_action(sites=[admin.site, site2, site3])
class TemplateAction(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"

    def has_permission(self):
        # Write your own logic here
        return super().has_permission()
```

## 4.8- Redirect Success Messages

You can define messges to be displayed to the user after form submission

- `post_success_message` attribute is used for `post` requests


**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action
from .my_sites import site2, site3

@register_quick_action()
class TemplateAction(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"
    post_success_message = "Data Submitted Successfully"

    # NOTE: Also you can override the messages using the following method
    # You can access the current request by using self.request
    def get_post_success_message(self):
        # Write your own logic here
```

---
**Notes**

1- **All actions must be added/imported in admin.py as to be detected and registered.**

## 4.9- URLs and Path Name

`url_path` is the URL path of an action, if not set the package will create a url path dynamically from the action class's name

`path_name` is the URL path name of an action, if not set the package will create a url path name dynamically from the action class's name


**Example 1:**

```python
from django.contrib import admin

from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action
from .my_sites import site2, site3

@register_quick_action()
class CreateUserTemplate(TemplateViewQuickAction):
    name = "My Template Action"
    template_name = "my_template.html"
```

- `url_path` value will be `www.mysite.com/admin/quick-actions/create-user-template`
- `path_name` value will be `quick-actions-create-user-template`


**Example 2:**

```python
from django.contrib import admin

from django_admin_performance_tools.quick_actions import TemplateViewQuickAction
from django_admin_performance_tools.quick_actions.registry import register_quick_action
from .my_sites import site2, site3

@register_quick_action()
class CreateUserTemplate(TemplateViewQuickAction):
    name = "My Template Action"
    url_path = "my-template"
    path_name = "my-template"
    template_name = "my_template.html"
```

- `url_path` value will be `www.mysite.com/admin/quick-actions/my-template`
- `path_name` value will be `quick-actions-my-template`


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

**Form Example:**

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
    def assign_user(self, request, queryset, submitted_form):
        # Write your own Logic
        user = submitted_form.cleaned_data.get("user")
        queryset.update(user=user)
```


**ModelForm Example:**

```python
from django import forms
from django.contrib import admin

from django_admin_performance_tools.intermediate_pages.decorators import intermediate_page
from django_admin_performance_tools.intermediate_pages.forms import IntermediatePageModelForm

from .models import MyModel

class MyForm(IntermediatePageModelForm):

    class Meta:
        model = MyModel
        fields = "__all__"

    def clean(self) -> dict[str, Any]:
        # Write your own Logic
        return super().clean()

    def save(self, commit: bool = ...) -> Any:
        # Write your own Logic
        return super().save(commit)

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):

    actions = ["create_object"]

    @intermediate_page(form=MyForm)
    def create_object(self, request, queryset, submitted_form):
        # Write your own Logic
        submitted_form.save()
```

-**IntermediatePageForm** is implemented on top of `forms.Form`

-**IntermediatePageModelForm** is implemented on top of `forms.ModelForm`

**Note**

`intermediate_page` decorator checks for form validity, it means that it will not continue to the action logic only if the form is valid.

### 6.1.1 intermediate_page decorator params

- **form** (required): A form inheriting from `IntermediatePageForm` or `IntermediatePageModelForm` that is passed to the intermediate page template to be rendered
- **template**: Path of an HTML template to use for rendering the intermediate page. defaults to `admin/intermediate_pages/abstract_form_page.html` that normally renders the form and shows selected objects if any
- **title**: Custom title for the intermediate page, defaults to the action name.
- **success_redirect_url**: URL to redirect after successful form submission defaults to the model change list page.


## 6.2- Non-Selection Actions

The existing Django actions require at least one selected instance to proceed, so
We introduce `Non-Selection Actions` for admin actions to proceed to the action without selecting any instances.

also Django admin actions are shown if there is at least one instance, but now all non-selection actions will be shown in actions dropdown even if there is no instances in change list page (and `Delete selected models` action will be excluded)

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

`No-Selection` actions overrides django `ChangeList` class (to show the actions when no instances in the changelist page) so if you've already override it simply you can inherits from `NoSelectionActionsChangeListMixin`


**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.mixins import NonSelectionActionsMixin, NoSelectionActionsChangeListMixin

from .models import MyModel

from django.contrib.admin.views.main import ChangeList

class MyChangeList(NoSelectionActionsChangeListMixin, ChangeList):
    # Your own logic

@admin.register(MyModel)
class MyModelAdmin(NonSelectionActionsMixin, admin.ModelAdmin):

    actions = ["assign_user"]
    non_selection_actions = ["assign_user"]

    def assign_user(self, request, queryset):
        # Write your own Logic

    def get_changelist(self, request, **kwargs):
        """
        Return the ChangeList class for use on the changelist page.
        """
        if self.non_selection_actions:
            return MyChangeList
        return ChangeList
```

![Alt text](/docs/images/non_selection_actions.gif?raw=true "Disabled Select")

## 6.3- Max Selection Count

The existing Django actions allows all staff users to select all the queryset and apply the action on it, imagine you have a 1 Million records and a staff user selected all the queryset and applied the action on it!

So ,We introduced `Max Selection Count` to set max instances to be selected to an action.

**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.decorators import check_queryset_max_selection

from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):

    actions = ["assign_user"]

    @check_queryset_max_selection(max_selection=100)
    def assign_user(self, request, queryset):
        # Write your own Logic
```

in case you want to customize `max_selection` based on the request you can pass a `function`/`lambda` that takes `request` as an argument instead of an `int` number.

if you set `max_selection` to `-1` means unlimited.

**Example:**

```python
from django.contrib import admin

from django_admin_performance_tools.decorators import check_queryset_max_selection

from .models import MyModel

def get_max_selection(request):
    if request.user.is_superuser:
        return 1000
    else:
        return 10

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):

    actions = ["assign_user"]

    @check_queryset_max_selection(max_selection=lambda request: get_max_selection(request))
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

## 8.1 Select Related with Filter Related Fields

Same as forms dropdowns, related filters get a list of instances and display its `__str__` function so if you access a related field  in the `__str__ ` it will hit the DB for each row in the related filter choices list.


So, We introduce `FilterWithSelectRelated` to select all related fields while rendering the filter choices

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
class MyModelAdmin(AdminChangeSelectRelatedMixin, admin.ModelAdmin):

    list_filter = [
        "another_model"
    ]
```

in the previous example, if we've 100 choice in the `another_model` filter list, it means that we've hit the DB 100 times, but by using `FilterWithSelectRelated` we can select `user` while rendering the choices.


**Example:**

```python
from django.contrib import admin
from django.contrin.auth.models import User
from django_admin_performance_tools.filters import FilterWithSelectRelated
from .models import MyModel, AnotherModel


class AnotherModel(models.Model):

    name = models.CharField()
    user = models.ForeignKey(User)

    def __str__(self):
        return f"{self.name} User: {self.user.username}"


class MyModel(models.Model):

    name = models.CharField()
    another_model = models.ForeignKey(AnotherModel)


class AnotherModelFilter(FilterWithSelectRelated):
    list_select_related = ["user"]


@admin.register(MyModel)
class MyModelAdmin(AdminChangeSelectRelatedMixin, admin.ModelAdmin):

    list_filter = [
        AnotherModelFilter
    ]
```


## 8.2 Search Help Text

Recently Django featured a new admin attribute `search_help_text` and it adds a help text below the search bar, So we extended this feature to be more useful and readable by showing all the fields that the admin will search in.

![Alt text](/docs/images/search_help_text.png?raw=true "Search Help Text")

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

**Upcomming**
- Auto Complete filters with custome title
- Filters with custom title

---

# 9- Widgets

Sometimes we may need to disable some choices of choice list fields based on who interacting with the field, for example: a super user can change status field to any choice but the staff user may have a limited options to change the status.


![Alt text](/docs/images/disabled_select.gif?raw=true "Disabled Select")


**Setup**

add `FORM_RENDERER` in `settings.py`.
```python
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
```

Add 'django.forms' to your INSTALLED_APPS settings.
```python
INSTALLED_APPS = [
    ...
    "django.forms",
]
```

**Example:**

```python

from django import forms
from django_admin_performance_tools.widgets import DisabledSelect
from django.db import models

class StatusEnum(models.IntegerChoices):
    INITIAL = 0, "Initial"
    DONE = 1, "Done"
    CLOSED = 2, "Closed"

class ContactForm1(forms.Form):
    status = forms.ChoiceField(
        required=False,
        choices=StatusEnum.choices,
        widget=DisabledSelect(disabled_options=[StatusEnum.DONE, StatusEnum.CLOSED])
    )
```
---

# 10- Settings

You can controll some behaves by adding the following in `settings.py`

**- HIDE_QUICK_ACTIONS_DROPDOWN**

This will hide the Quick Actions dropdown from admin sites

Default value is `False`


**- QUICK_ACTIONS_URL_PATH_PREFIX**

This is the prefix before all Quick-Actions URL paths/names

Default value is `quick-actions`


**- HIDE_LANGUAGE_DROPDOWN**

This will hide the Languages dropdown from admin sites

Default value is `False`


[github-repo]: https://github.com/muhammedattif/Django-Admin-Performance-Tools
[django-formtools]: https://pypi.org/project/django-formtools/


## Contributing

If you are interested to fix an issue or to add new feature, you can just open a pull request.

### Contributors
<a href = "https://github.com/muhammedattif/Django-Admin-Performance-Tools/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=muhammedattif/Django-Admin-Performance-Tools"/>
</a>
