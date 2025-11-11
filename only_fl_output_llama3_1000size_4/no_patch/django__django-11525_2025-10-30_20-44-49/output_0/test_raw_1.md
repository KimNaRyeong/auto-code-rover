Here is the reproducer script:

```python
import django
from django.core.mail import mail_managers, BadHeaderError
from django.conf import settings
from django.utils.functional import SimpleLazyObject

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
    settings.configure()
    settings.MANAGERS = ['one@example.com', 'two@example.com']
    try:
        mail_managers()
    except BadHeaderError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the `MANAGERS` setting to an improper format and then calls `mail_managers()`. If the issue is present, it prints a stack trace using the provided function and raises an `AssertionError`.