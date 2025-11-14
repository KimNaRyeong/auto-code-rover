Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
This script defines a `DurationFieldForm` with a single `duration` field, and then creates an instance of the form with the problematic input string `'P3(3D'`. It then calls `full_clean()` on the form, which should raise a `ValueError` when trying to parse the broken data. The script catches the exception, prints the stack trace using the provided function, and then raises an `AssertionError` to indicate that the issue is present.

If the issue is fixed, the script will exit with code 0.