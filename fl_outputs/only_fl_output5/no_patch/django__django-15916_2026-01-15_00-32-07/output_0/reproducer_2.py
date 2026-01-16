"""
reproducer.py
This script aims to demonstrate an issue where Django's `modelform_factory` does not use
`formfield_callback` specified in a `ModelForm`'s Meta class.
"""

import sys

def setup_django_environment():
    from django.conf import settings

    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_I18N=True,
        USE_TZ=True,
    )

    import django
    django.setup()

setup_django_environment()

from django import forms
from django.db import models

# Define a minimal model for testing
class MyModel(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'myapp'

def all_required(field, **kwargs):
    """A simple callback function to make form fields required."""
    formfield = field.formfield(**kwargs)
    if formfield:  # Ensure formfield is not None
        formfield.required = True
    return formfield

class MyForm(forms.ModelForm):
    """A custom ModelForm with a formfield_callback defined in Meta."""

    class Meta:
        model = MyModel
        fields = ['active', 'name']
        formfield_callback = all_required

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# The test function to reproduce the issue
def test_formfield_callback_issue():
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    test_form = FactoryForm()

    # Asserting that all fields in the generated form are required (as per our all_required callback)
    for field_name, field in test_form.fields.items():
        if not field.required:
            raise AssertionError(f"Field '{field_name}' is not required but should be.")

try:
    test_formfield_callback_issue()
    print("The issue seems to be fixed, as the test passed without errors.")
    sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
