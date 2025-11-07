Here is the reproducer script:

```python
import django
from django.db import models

def model_to_dict(instance, fields=None):
    if fields and hasattr(instance, 'fields') and instance.fields:
        return {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name not in fields}
    else:
        return {}

class MyModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)

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

def test_model_to_dict():
    try:
        model_to_dict(MyModel(), [])
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    test_model_to_dict()
```

This script should reproduce the issue by calling `model_to_dict` with an empty list of fields and asserting that it raises an `AssertionError`.