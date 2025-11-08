Here is the reproducer script:

```python
import django
from django import forms
from django.db import models

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield

class MyModel(forms.ModelForm):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        model = MyModel
        fields = ['active', 'name']
        formfield_callback = all_required

class MyForm(MyModel):
    class Meta:
        formfield_callback = all_required

FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

try:
    form = FactoryForm()
    assert not form.fields['active'].required
    print_stacktrace(AssertionError("Expected 'active' field to be required"))
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script creates a `MyModel` and its corresponding forms (`MyForm` and `FactoryForm`). It then asserts that the `'active'` field in the `FactoryForm` is not required, which should raise an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.