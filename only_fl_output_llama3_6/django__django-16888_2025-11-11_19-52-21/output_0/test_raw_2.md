Here is the reproducer script:

```python
import decimal
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

def test_invalid_decimal_query():
    try:
        model = DecimalModel(dec_field='12345')
        model.save()
        model.objects.get(dec_field='12346')
    except decimal.InvalidOperation as e:
        print_stacktrace(e)
        raise AssertionError("Too large decimal query caused exception.")
    except Exception as e:
        print_stacktrace(e)
        raise

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

if __name__ == "__main__":
    try:
        test_invalid_decimal_query()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(0)
```

This script should reproduce the issue and raise an `AssertionError` when the issue is present.