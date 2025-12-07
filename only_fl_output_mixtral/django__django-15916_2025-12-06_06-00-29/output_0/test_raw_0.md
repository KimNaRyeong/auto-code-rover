 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
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
