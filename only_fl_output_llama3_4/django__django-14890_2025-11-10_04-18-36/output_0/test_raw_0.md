Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

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
        class MyModel(models.Model):
            name = models.CharField()

        for name in ['a', 'b', 'c']:
            MyModel.objects.create(name=name)

        group1 = MyModel.objects.filter(name='a')
        group2 = MyModel.objects.filter(name='b')
        group3 = MyModel.objects.filter(name='c')

        combined_group = group1.union(group2)
        assert not (combined_group & group1).filter().exists(), "Expected an error"
        assert not (combined_group | group3).filter().exists(), "Expected an error"

    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, creates some test data, and then attempts to use the `union`, `&` (intersection), and `|` (union) operators on QuerySets. If any of these operations succeed without raising an error, it means that the issue is present.