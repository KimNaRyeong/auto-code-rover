Here is the reproducer script:

```python
import django
from django.db import models
from django.forms import Form, ModelForm
from django.test import TestCase

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

def setup_django():
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testbed.settings'

setup_django()
django.setup()

class MyModel(models.Model):
    some_field = models.CharField(max_length=255, default='default_value')

class MyForm(ModelForm):
    class Meta:
        model = MyModel
        fields = ['some_field']

class TestIssue(TestCase):
    def test_issue(self):
        my_form = MyForm({'other_field': 'value'})
        if not hasattr(my_form, '_errors'):
            my_form._errors = {}
        my_form.full_clean()
        self.assertEqual(my_form.cleaned_data['some_field'], 'default_value')

if __name__ == '__main__':
    try:
        TestIssue().test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed. Issue not present.")
        exit(0)

```

This script sets up the Django environment before running the test, which should reproduce the issue.