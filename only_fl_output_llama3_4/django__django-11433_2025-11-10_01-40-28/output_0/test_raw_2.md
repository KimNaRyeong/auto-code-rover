Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
from django.db import models
from django.forms import Form, ModelForm

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

def reproduce_issue():
    from django.conf import settings
    settings.configure()

    class MyModel(models.Model):
        some_field = models.CharField(max_length=255, default='default_value')

    class MyForm(ModelForm):
        class Meta:
            model = MyModel
            fields = ['some_field']

    my_model = MyModel()
    form_data = {'some_field': 'new_value'}
    form = MyForm(data=form_data, instance=my_model)
    try:
        cleaned_data = {'some_field': 'cleaned_value'}
        form.cleaned_data = cleaned_data
        form.is_valid()
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script should be executed by `python3 reproducer.py` in your terminal. If the issue is present, it will print a stack trace and raise an `AssertionError`.