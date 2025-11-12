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
        formfield_callback = all_required
        fields = ['active', 'name']

def main():
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)
    my_form = FactoryForm()
    assert not my_form.fields['active'].required, "Expected the field to be required"
    print_stacktrace(AssertionError("Expected the field to be required"))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script creates a `MyModel` and a `MyForm`, which inherits from `forms.ModelForm`. The `formfield_callback` is set to `all_required`, which makes all form fields required. Then, it uses the `modelform_factory` function to create a new form class based on `MyModel` and `MyForm`. It then creates an instance of this form and asserts that the 'active' field is not required. If the assertion fails (i.e., the field is actually required), it prints the stack trace and exits with code 1.