Here is the reproducer script:

```python
import django
from django.db.models import Q, F
from django.db.models.expressions import OrderBy

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
    
    class Model(django.db.models.Model):
        class Meta:
            ordering = ['id']

    queryset = Model.objects.all().order_by('-id')

    assert not hasattr(queryset.query, '_order'), "Ordering is mutable"
    print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

This script sets up a Django project, defines a simple model with ordering set to 'id', and then tries to order the queryset in reverse. If the issue is present, it should raise an `AssertionError` and print the stack trace.