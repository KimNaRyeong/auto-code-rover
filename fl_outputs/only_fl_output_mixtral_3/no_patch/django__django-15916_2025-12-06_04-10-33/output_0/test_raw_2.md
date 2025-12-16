 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
from django import forms
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield

class MyForm(forms.ModelForm):
    formfield_callback = all_required
    class Meta:
