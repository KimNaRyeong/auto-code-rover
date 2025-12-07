 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

    def clean_fields(self, exclude=None):
        # Avoid calling super() to prevent infinite recursion
        if not exclude or 'value' not in exclude:
            try:
                Decimal(self.value)
            except ValidationError:
                raise ValidationError({'value': 'Invalid decimal value'})

def create_and_retrieve_mymodel():
    obj = MyModel.objects.create(value="nan")
    obj.save()
    try:
        MyModel.objects.get(pk=obj.pk)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    create_and_retrieve_mymodel()
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.