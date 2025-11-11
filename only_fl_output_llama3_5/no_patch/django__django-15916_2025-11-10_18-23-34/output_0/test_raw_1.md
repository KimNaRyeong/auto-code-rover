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

def test_issue():
    from django.forms import modelform_factory
    FactoryForm = modelform_factory(MyModel, form=MyForm)
    my_form = FactoryForm()
    assert not my_form.fields['active'].required and not my_form.fields['name'].required
    raise AssertionError("Expected fields to be required")

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script will run the `test_issue` function, which creates a form using the `modelform_factory` and checks if the fields are required. If they are not, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.