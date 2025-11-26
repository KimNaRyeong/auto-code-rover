Here is the `reproducer.py` file that reproduces the issue:
```
import sys
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
        formfield_callback = all_required
        fields = ['active', 'name']

FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

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

try:
    form = FactoryForm()
    assert form.fields['active'].required, "Field 'active' is not required"
    assert form.fields['name'].required, "Field 'name' is not required"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script defines a `MyModel` with two fields, and a `MyForm` that uses the `all_required` callback to make both fields required. The `modelform_factory` is used to create a new form class `FactoryForm`. The script then creates an instance of `FactoryForm` and checks if both fields are required. If not, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1. If the issue is fixed, the script will exit with code 0.