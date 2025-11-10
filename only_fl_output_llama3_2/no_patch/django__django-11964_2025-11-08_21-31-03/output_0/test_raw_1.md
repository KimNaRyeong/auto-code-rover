Here is the reproducer script:

```python
import django
from django.db import models
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

def main():
    try:
        from testing.pkg.models import MyObject, MyChoice
        my_object = MyObject(my_str_value=MyChoice.FIRST_CHOICE)
        assert str(my_object.my_str_value) == "first"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script should reproduce the issue by asserting that the value of `my_str_value` is equal to `"first"`, which will fail because the actual value is `'MyChoice.FIRST_CHOICE'`.