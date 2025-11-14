Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import django
from django.conf import settings
from django.forms import forms
from django.utils.dateparse import parse_duration

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

def test_duration_field():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    django.setup()
    
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
This script sets up the Django environment by setting the `DJANGO_SETTINGS_MODULE` environment variable and calling `django.setup()`. It then defines a `DurationFieldForm` with a single `duration` field, creates an instance of the form with the problematic input string `'P3(3D'`, and calls `full_clean()` on the form. If the issue is present, it should raise a `ValueError` when trying to parse the broken data, which will be caught and printed along with the stack trace using the provided function. Finally, an `AssertionError` will be raised to indicate that the issue is present.

If the issue is fixed, the script will exit with code 0.