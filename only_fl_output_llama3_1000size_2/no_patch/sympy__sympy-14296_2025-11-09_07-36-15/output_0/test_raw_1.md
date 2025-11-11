Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp
from collections import defaultdict, Iterable

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

def reproduce_issue():
    b = sp.Rational(1) - sp.sqrt(2)
    a = sp.to_number_field(b)
    assert str(a.minpoly) == 'x**2 + 2*x - 1', "Issue: Minimal polynomial of algebraic number is incorrect"
    raise AssertionError("Issue reproduced")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `reproduce_issue` function, which creates an algebraic number and then checks if its minimal polynomial is correct. If not, it raises an `AssertionError`, which is caught by the script and printed with a stack trace.