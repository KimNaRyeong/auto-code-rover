Here's a standalone Python file named `reproducer.py` that aims to reproduce the issue described. This script checks whether the `formfield_callback` function is correctly used by the `FactoryForm` generated from `modelform_factory` with a custom `ModelForm`. If the issue is present (i.e., `FactoryForm` fails to use the specified `formfield_callback`), the script will raise an `AssertionError` and print a detailed stack trace of the issue.

```python
from django import forms
from django.db import models

# Setup Django environment
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


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
        model = MyModel
        fields = ['active', 'name']

# A counter to track the number of times `all_required` is called.
global callback_counter
callback_counter = 0

def all_required_counter(field, **kwargs):
    global callback_counter
    callback_counter += 1
    return all_required(field, **kwargs)


def print_stacktrace(e: Exception):
    import traceback
    import sys

    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


# Run test to reproduce the bug
def test_formfield_callback_usage():
    global callback_counter
    FactoryForm = forms.modelform_factory(MyModel, form=MyForm, formfield_callback=all_required_counter)
    form = FactoryForm()
    # Since there are two fields (`active`, `name`) in `MyModel`,
    # and if `all_required_counter` is called correctly for each,
    # then `callback_counter` should be 2.
    try:
        assert callback_counter == 2, "Formfield callback not used correctly for each field."
        print("Issue not present. Formfield callback works as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_formfield_callback_usage()
    except AssertionError:
        # Exit with a non-zero code to indicate failure
        raise SystemExit(1)
```

Please note, for this script to work, Django needs to be setup and configured correctly in your project. Specifically, you must have a Django project with an appropriately configured settings module (`"project.settings"` in this case, which you might need to adjust according to your project's structure).

If the issue described is present, the script will raise an `AssertionError` indicating "Formfield callback not used correctly for each field." and then exit with code 1. If the issue is fixed, it prints "Issue not present. Formfield callback works as expected." and exits with code 0.