Here is the reproducer script:

```python
import sys
from fractions import Fraction as F

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
    x = F(1)
    if not (x in [F(i) for i in range(2, 10)]):
        raise AssertionError("Issue present")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue fixed")
    sys.exit(0)
```

This script will attempt to reproduce the issue by checking if `x` is in a list of fractions from 2 to 9. If the issue is present, it will raise an `AssertionError` and print the stack trace. If the issue is fixed, it will print "Issue fixed" and exit with code 0.