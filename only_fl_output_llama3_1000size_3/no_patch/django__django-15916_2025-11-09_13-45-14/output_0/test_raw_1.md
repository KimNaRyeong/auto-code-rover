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
    formfield_callback = all_required

    class Meta:
        model = MyModel
        fields = ['active', 'name']

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

try:
    from django.forms import modelform_factory
except ImportError as e:
    print_stacktrace(e)
    exit(1)

try:
    form = modelform_factory(MyModel, form=MyForm)()
    assert not any(f.field.required for f in form), "Expected all fields to be required"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.