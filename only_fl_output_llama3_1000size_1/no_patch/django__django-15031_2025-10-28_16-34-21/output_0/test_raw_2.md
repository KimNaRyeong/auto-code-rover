Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    if value.startswith('[') and value.endswith(']'):
        return [x.strip() for x in value[1:-1].split(',')]
    elif ',' in value:
        raise ValueError("Invalid lookup value: %r" % value)
    else:
        return [value]

def main():
    try:
        admin.site.register(User)
        User.objects.filter(username__in='johnny,viola,gordon')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()

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
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script will attempt to register the `User` model with the Django admin site and then filter it by username using the `username__in` lookup. If the issue is present, it should raise a `ValueError` due to the comma in the value string. The `print_stacktrace` function will then print the stack trace of the error.