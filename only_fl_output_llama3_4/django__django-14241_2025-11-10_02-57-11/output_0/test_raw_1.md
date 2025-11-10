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

        result = list(qs1.union(qs2).values_list('name'))
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        if len(result) != 0:
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

This script creates two mock models, Celebrity and ReservedName. It then combines the querysets of these models using the union method and tries to execute a values_list operation on the result. If an exception is raised during this process, it prints the stack trace and raises the exception again.