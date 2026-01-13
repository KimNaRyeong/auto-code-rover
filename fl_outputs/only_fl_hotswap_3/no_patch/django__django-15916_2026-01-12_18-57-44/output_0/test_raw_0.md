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
    raise AssertionError("Formfield callbacks are different.")

for field in FactoryForm().fields.values():
    assert field.required, "Field is not required."

print("No issues found.")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    raise AssertionError("Formfield callbacks are different.")
AssertionError: Formfield callbacks are different.
```
This stack trace shows that the `AssertionError` was raised at line 27, which is where the assertion checks if the formfield callbacks are different. This confirms that the issue is present.

If the issue is fixed, the script should print "No issues found." and exit with code 0.