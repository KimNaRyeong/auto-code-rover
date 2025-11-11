Here is the reproducer script:

```python
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

class MyModel(models.Model):
    some_field = models.CharField(max_length=255, default='default_value')

class MyForm(ModelForm):
    class Meta:
        model = MyModel
        fields = ['some_field']

class TestIssue(TestCase):
    def test_issue(self):
        my_form = MyForm({'another_field': 'value'})
        my_model = MyModel()
        if not hasattr(my_model, 'cleaned_data'):
            raise AssertionError("Expected 'cleaned_data' attribute on MyModel")
        with self.assertRaises(AssertionError):
            try:
                my_model.some_field = my_form.cleaned_data.get('some_field', None)
                print_stacktrace(AssertionError('Expected some_field to be overwritten'))
            except Exception as e:
                raise

if __name__ == '__main__':
    TestIssue().test_issue()
```

This script creates a Django model and form, then attempts to overwrite the default value of `some_field` on the model using the cleaned data from the form. If the issue is present (i.e., the default value cannot be overwritten), an `AssertionError` will be raised with a stack trace printed.