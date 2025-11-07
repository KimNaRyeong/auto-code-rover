Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.models import Exists, BooleanField
from django.db.models.functions import Coalesce

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

class A(models.Model):
    pass

class B(models.Model):
    pass

def main():
    A.objects.create()
    B.objects.create()

    result = A.objects.annotate(should_be_bool=Coalesce(Exists(B.objects.none()), False)).first().should_be_bool
    if result is not None and not isinstance(result, bool):
        raise AssertionError("Expected a boolean value, got {}".format(result))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
    main()
```

This script creates two models `A` and `B`, then annotates a query on model `A` with the result of an `Exists` query on model `B`. The `Coalesce` function is used to return `False` if the `Exists` query returns `None`. If the result is not a boolean value, it raises an `AssertionError`.

Please note that this script should be run in the root directory of your Django project.