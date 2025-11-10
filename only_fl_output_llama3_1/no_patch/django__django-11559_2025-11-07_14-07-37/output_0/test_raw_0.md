Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.expressions import F, Value
from django.db.models.query_utils import Q

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
    class ParentModel(models.Model):
        class Meta:
            ordering = ['expression()']

    class ChildModel(ParentModel):
        pass

    try:
        ChildModel.objects.order_by('expression')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script sets up a simple Django project, defines two models with inheritance (`ParentModel` and `ChildModel`), and then tries to order the child model by an expression. If the issue is present, it will print the stack trace and raise an assertion error.