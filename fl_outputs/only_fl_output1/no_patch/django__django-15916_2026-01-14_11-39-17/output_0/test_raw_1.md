Given the feedback and the need to avoid relying on an existing Django project configuration (e.g., `project.settings`), we can attempt to reproduce the issue with a slightly modified approach that doesn't require an external Django project setup. This approach will still demonstrate the problem by manually checking if the `formfield_callback` specified in the `Meta` class of `MyForm` is respected.

Let's use the Django's `settings.configure()` function to setup a minimal runnable environment inline, avoiding dependencies on an external project setting.

```python
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django import forms

# Configuring Django settings (minimal configuration)
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # this script will be the "app"
    ),
    USE_TZ=True,  # Set to True to avoid warnings, adjust to your needs
)

# Explicitly setting up Django (required for standalone scripts)
django.setup()

# Define your models and forms here
class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        app_label = '__main__'  # Required for standalone scripts to simulate an app


# Your custom formfield callback
def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield


# ModelForm definition
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['active', 'name']
        formfield_callback = all_required


# Function to print the stack trace of exceptions
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Testing function to use the formfield_callback from Meta
def test_factory_form():
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    form_instance = FactoryForm()

    for field_name in form_instance.fields:
        if not form_instance.fields[field_name].required:
            raise AssertionError(f"Field '{field_name}' is not marked as required.")

    print("All fields are correctly marked as required - Issue not present.")

if __name__ == '__main__':
    try:
        test_factory_form()
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

Ensure you have Django installed in your Python environment. If Django is not installed, you can install it using pip:

```
pip install django
```

Here's an explanation of key changes and considerations:

- The script now uses Django's `settings.configure()` to set up a minimal, inline Django environment needed to run the model and form definitions without relying on an external Django project.
- The `app_label = '__main__'` meta option in `MyModel` class allows us to define models in a script without a formal Django app structure.
- The testing function `test_factory_form()` attempts to create a form using `modelform_factory` and checks if the fields are required, as intended by the `formfield_callback` specified in `MyForm.Meta`.
- An assertion check within `test_factory_form()` directly verifies if the issue is present, without relying on Django's full framework execution flow or external project settings.

This script can function as a standalone Django setup to test the specific behavior in question.