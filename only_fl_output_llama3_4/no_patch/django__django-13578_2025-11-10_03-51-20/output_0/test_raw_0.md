Here is the reproducer script:

```python
import django
from django.forms import FormSet
from django.test.utils import override_settings

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

def main():
    django.setup()
    class SomeFormSet(FormSet):
        def __init__(self, *args, **kwargs):
            super(SomeFormSet, self).__init__(*args, **kwargs)
            self.prefix = 'articles'

    formset = SomeFormSet(prefix='wrong_prefix')
    try:
        formset.is_valid()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected ManagementForm exception")

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines a custom `SomeFormSet` class that inherits from Django's `FormSet`, and then attempts to validate the formset with an incorrect prefix. If the expected exception is not raised, it will raise an `AssertionError`.