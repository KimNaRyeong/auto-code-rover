Here is the reproducer script:

```python
import sys
from QQ.frac_field import FractionField as FF

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

try:
    FF(1/0)  # This should raise an AssertionError
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue fixed!")
    sys.exit(0)
```

This script tries to create a `FractionField` with the fraction `1/0`, which should raise an `AssertionError`. If it does, the script prints the stack trace and exits with code 1. If it doesn't (i.e., the issue is fixed), the script prints "Issue fixed!" and exits with code 0.