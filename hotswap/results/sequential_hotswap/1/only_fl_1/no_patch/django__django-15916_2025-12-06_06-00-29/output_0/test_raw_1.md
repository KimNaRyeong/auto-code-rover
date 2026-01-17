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
    raise AssertionError("Formfield callback is not correctly set in FactoryForm")

for field in FactoryForm().fields.values():
    assert field.required, "All fields should be required"
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    raise AssertionError("Formfield callback is not correctly set in FactoryForm")
AssertionError: Formfield callback is not correctly set in FactoryForm
```
This stack trace shows that the issue is present in the `forms.modelform_factory` function, which does not correctly set the `formfield_callback` attribute in the returned form class.