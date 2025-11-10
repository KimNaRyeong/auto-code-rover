Here is the reproducer script in Python:

```python
import django
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _

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

def reproducer():
    # Create a formset with no management form
    MyFormSet = inlineformset_factory(None, None, BaseFormSet)
    formset = MyFormSet()

    try:
        formset.management_form.cleaned_data[BaseFormSet._default_key] = 0
        formset.is_valid()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    django.setup()  # Initialize Django
    reproducer()
```

This script creates a formset with no management form, then sets the `TOTAL_FORM_COUNT` key in the management form's cleaned data to 0. It then calls `is_valid()` on the formset. If an exception is raised, it prints the stack trace and raises an `AssertionError`.