Here is the reproducer script:

```python
import django
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

FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

try:
    form = FactoryForm()
    assert not form.fields['active'].required
    print_stacktrace(AssertionError("Expected 'active' field to be required"))
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
except Exception as e:
    print_stacktrace(e)
    exit(1)

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

```

This script creates a `MyModel` and its corresponding forms (`MyForm` and `FactoryForm`). It then asserts that the `'active'` field in the `FactoryForm` is not required, which should raise an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.