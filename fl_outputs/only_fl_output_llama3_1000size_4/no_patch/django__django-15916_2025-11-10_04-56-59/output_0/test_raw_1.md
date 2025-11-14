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

def main():
    try:
        from django.forms import modelform_factory
        FactoryForm = modelform_factory(MyModel, form=MyForm)
        my_form = FactoryForm()
        assert not my_form.fields['active'].required and not my_form.fields['name'].required, "Expected fields to be required"
        print_stacktrace(AssertionError("Expected fields to be required"))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.