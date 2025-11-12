Here is the reproducer script in a code block:

```python
import django
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory
from django.db import models

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
    class MyModel(models.Model):
        pass

    MyFormSet = inlineformset_factory(MyModel, None, BaseFormSet)

    formset = MyFormSet()

    try:
        formset.is_valid()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a custom model and form set using Django's inlineformset_factory. It then attempts to validate the empty form set, which should raise an exception due to the absence of management form data. The reproducer script catches this exception, prints the stack trace, and raises an AssertionError if the issue is present.