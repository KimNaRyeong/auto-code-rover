Here is the reproducer script:

```python
import sys
from combinatorics import Schur_Number

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
    Schur_Number(1)  # This should raise an AssertionError
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(0)
```

This script will attempt to create a `Schur_Number` object with the argument `1`. If this raises an `AssertionError`, it will print the stack trace and exit with code 0.