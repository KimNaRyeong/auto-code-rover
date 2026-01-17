```python
# reproducer.py
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps
import sys

apps.populate(settings.INSTALLED_APPS)

class MyModel(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        app_label = 'myapp'

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    if formfield:  # Ensure the form field can be created
        formfield.required = True
    return formfield

class MyForm(forms.ModelForm):
    formfield_callback = all_required
    class Meta:
        model = MyModel
        fields = ['active', 'name']

FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

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

def test_formfield_callback():
    form = FactoryForm()
    active_field = form.fields.get('active', None)
    name_field = form.fields.get('name', None)
    if active_field and name_field:
        if not active_field.required or not name_field.required:
            raise AssertionError("FactoryForm fields are not marked as required.")
    else:
        raise AssertionError("Could not find the expected fields in FactoryForm.")

if __name__ == "__main__":
    try:
        test_formfield_callback()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    print("No issues detected.")
    sys.exit(0)
```

This script checks if the `formfield_callback` specified in the `Meta` class of a `ModelForm` is used correctly when generating forms using the `modelform_factory` function in Django. If the fields `'active'` and `'name'` in the dynamically generated `FactoryForm` are not marked as required, which `all_required` formfield_callback is supposed to do, it raises an `AssertionError`. The error along with the stack trace is printed if the test fails, indicating the issue is present. If the test passes, it prints "No issues detected" and exits with code `0`, indicating the issue has been fixed. 

Please note this script is designed to run in a Django project environment. Make sure `myapp` is in your `INSTALLED_APPS` within your Django settings, or adjust the `app_label` in `MyModel.Meta` appropriately to match your project setup.