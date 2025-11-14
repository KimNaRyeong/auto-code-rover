Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.db.models.fields import DecimalField
from django.core.exceptions import ValidationError

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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nanbug.settings')
    from django.conf import settings
    settings.configure()
    from django.db.models.base import ModelBase

    class DecimalField(models.Field):
        def to_python(self, value):
            if value is None:
                return None
            try:
                return float(value)
            except ValueError:
                raise ValidationError('Invalid decimal value')

    class MyModel(ModelBase):
        value = models.DecimalField(max_digits=10, decimal_places=5)

    model = MyModel()
    model.value = float('nan')
    try:
        model.save()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the `DecimalField` and `MyModel`, creates an instance of `MyModel` with a NaN value for its `value` field, and attempts to save it. If any exception occurs during this process (which should be the case since storing NaN in a DecimalField is not allowed), the script prints the stack trace and exits with code 1.