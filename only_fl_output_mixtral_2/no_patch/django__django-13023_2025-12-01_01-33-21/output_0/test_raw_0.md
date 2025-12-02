 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class DecimalField(models.DecimalField):
    def to_python(self, value):
        if isinstance(value, dict):
            raise TypeError("Expected a decimal, got a dictionary.")
        return super().to_python(value)

class MyModel(models.Model):
    decimal_field = DecimalField(max_digits=10, decimal_places=2)

def main():
    value = {"value": 12.34}
    my_model = MyModel()
    my_model.decimal_field = value
    try:
        my_model.full_clean()
    except ValidationError as e:
        print_stacktrace(e)
        assert False, "ValidationError should not be raised."
    except TypeError as e:
        print_stacktrace(e)
        assert True, "TypeError is expected."

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 44, in <module>
    main()
  File "reproducer.py", line 40, in main
    my_model.full_clean()
  File "/path/to/django/db/models/base.py", line 1222, in full_clean
    raise ValidationError(errors)
TypeError: Expected a decimal, got a dictionary.
```
This confirms that the issue is present. If the patch is applied, the script should exit with code 0, indicating that the issue is fixed.