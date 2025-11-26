Here is the revised `reproducer.py` file that reproduces the issue:
```
import os
import django
from django.conf import settings
from django.forms.formsets import formset_factory, ManagementForm
from django import forms

def main():
    # Configure Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
    django.setup()

    # Create a sample form
    class SampleForm(forms.Form):
        name = forms.CharField()

    # Create a sample formset
    SampleFormSet = formset_factory(SampleForm)

    try:
        # Reproduce the issue by specifying the prefix incorrectly
        formset = SampleFormSet({'articles-0-name': 'Test'}, 'articles')
        formset.is_valid()
        raise AssertionError("Issue not reproduced")
    except django.core.exceptions.ValidationError as e:
        print_stacktrace(e)
        assert "ManagementForm data is missing or has been tampered with" in str(e), "Issue not reproduced"
        print("Issue reproduced successfully")
        return 1
    else:
        print("Issue fixed, no error raised")
        return 0

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

if __name__ == "__main__":
    exit(main())
```
This script configures Django settings before creating the form and formset, which should fix the `ImproperlyConfigured` error. It then attempts to reproduce the issue by specifying the prefix incorrectly when validating the formset. If the issue is present, it should raise a `ValidationError` with the message "ManagementForm data is missing or has been tampered with", which we assert on. If the assertion passes, we print a success message and exit with code 1. If the issue is fixed, no error will be raised, and we'll print a success message and exit with code 0.