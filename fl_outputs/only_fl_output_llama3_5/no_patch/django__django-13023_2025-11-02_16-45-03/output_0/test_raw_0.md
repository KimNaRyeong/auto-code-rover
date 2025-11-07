Here is the reproducer script:

```python
import django
from django.db import models

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
    django.setup()
    class MyModel(models.Model):
        decimal_field = models.DecimalField(max_digits=5, decimal_places=2)

    try:
        my_model = MyModel(decimal_field={'a': 1})
        my_model.to_python()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError"
        exit(0)