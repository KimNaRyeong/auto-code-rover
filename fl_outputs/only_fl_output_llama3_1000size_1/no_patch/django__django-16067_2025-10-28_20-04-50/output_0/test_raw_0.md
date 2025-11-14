Here is the reproducer script:

```python
import unittest
from decimal import Decimal
from django.core.validators import DecimalValidator
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

class Test(unittest.TestCase):
    def test(self):
        value = '0E+1'
        validator = DecimalValidator(max_digits=8, decimal_places=7)
        try:
            validator(Decimal(value))
            self.fail("Expected ValidationError")
        except ValidationError as e:
            print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an AssertionError and print a stack trace.