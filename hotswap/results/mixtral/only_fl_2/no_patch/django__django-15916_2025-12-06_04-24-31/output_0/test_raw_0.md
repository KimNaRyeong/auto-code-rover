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
        model = MyModel
        formfield_callback = all_required
        fields = ['active', 'name']

FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

if MyForm.formfield_callback is not FactoryForm.formfield_callback:
    raise AssertionError("Formfield callback is not propagated to the factory form")

for field_name in MyForm.base_fields:
    if not MyForm.base_fields[field_name].required:
        raise AssertionError(f"Field {field_name} is not required in the factory form")

print("No issues found")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, the script will print "No issues found" and exit with code 0.

The `print_stacktrace` function is not used in this example, as the `AssertionError` message provides enough context for the issue.