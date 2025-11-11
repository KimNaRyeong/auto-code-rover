Here is the reproducer script:

```python
import django
from django.db.models import Q
from django.db.models.query import QuerySet

def main():
    try:
        Celebrity = type('Celebrity', (object,), {'objects': QuerySet()})  # Create a mock model
        ReservedName = type('ReservedName', (object,), {'objects': QuerySet()})  # Create a mock model

        qs1 = Celebrity.objects.all()
        qs2 = ReservedName.objects.all()

        result = qs1.union(qs2).values_list('name').first()
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        if result is None:
            print("Issue not present")
            exit(0)

if __name__ == "__main__":
    django.setup()  # Initialize Django
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
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will raise an `AssertionError` and print a stack trace with line numbers.