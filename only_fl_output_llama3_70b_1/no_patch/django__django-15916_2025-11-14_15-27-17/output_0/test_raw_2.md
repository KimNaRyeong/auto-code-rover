Here is the revised `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.conf import settings
from django import forms
from django.db import models

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield

class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)

class MyForm(forms.ModelForm):
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

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth'
    ]
)

try:
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    form = FactoryForm()
    assert form.fields['active'].required, "Field 'active' is not required"
    assert form.fields['name'].required, "Field 'name' is not required"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue is fixed")
    sys.exit(0)
```
This script sets up a minimal Django environment and defines the `MyModel` and `MyForm` classes. It then creates an instance of `FactoryForm` using `modelform_factory` and checks if both fields are required using assertions. If either field is not required, an `AssertionError` is raised, and the script prints the stack trace using the provided `print_stacktrace` function. If the issue is fixed, the script exits with code 0.

Please note that you need to create a `settings.py` file in the same directory as this script, with at least the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth'
]
```