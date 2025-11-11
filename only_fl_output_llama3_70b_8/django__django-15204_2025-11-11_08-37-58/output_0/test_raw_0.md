Here is the `reproducer.py` file that reproduces the issue:
```
import django
from django import forms
from django.utils.dateparse import parse_duration

def test_duration_field():
    class DurationFieldForm(forms.Form):
        duration = forms.DurationField()

    form = DurationFieldForm({'duration': 'P3(3D'})
    try:
        form.full_clean()
    except ValueError as e:
        print_stacktrace(e)
        assert False, "DurationField.clean fails to handle broken data"

if __name__ == "__main__":
    test_duration_field()
```
This script defines a `DurationFieldForm` with a single field `duration`, and then creates an instance of the form with the input string `'P3(3D'`. It then calls `full_clean()` on the form, which should raise a `ValueError` when trying to parse the broken duration string. The `print_stacktrace` function is used to print the stack trace of the exception, and the script asserts that the issue is present.

To run this script, save it as `reproducer.py` in the root directory of your Django project, and execute it with `python3 reproducer.py`. If the issue is present, the script should raise an `AssertionError` and print a stack trace. If the issue is fixed, the script should exit with code 0.