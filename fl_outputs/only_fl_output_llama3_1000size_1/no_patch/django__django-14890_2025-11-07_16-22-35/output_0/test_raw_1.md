Here is the reproducer script:

```python
import django
from django.db.models import Q, QuerySet
from django.db.models.query import QuerySet

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
        django.setup()
        
        class MyModel(django.db.models.Model):
            name = django.db.models.CharField(max_length=255)

        for name in ['a', 'b', 'c']:
            MyModel.objects.create(name=name)

        group1 = MyModel.objects.filter(name='a')
        group2 = MyModel.objects.filter(name='b')
        group3 = MyModel.objects.filter(name='c')

        combined_group = group1.union(group2)
        assert not (combined_group & group1).filter().exists(), "Expected an error"
        print_stacktrace(AssertionError("Expected an error"))

    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script sets up Django before creating the model and querysets. This should allow the issue to be reproduced correctly.