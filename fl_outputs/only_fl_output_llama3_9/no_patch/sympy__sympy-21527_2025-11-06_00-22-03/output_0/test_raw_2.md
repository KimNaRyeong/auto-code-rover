Here is the reproducer script:

```python
import sympy
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    for i in [0.0215, 0.0216, 0.0217]:
        x,y = sympy.symbols('x, y')
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, i * x)], (x, y))
        if not isinstance(result, sympy.sets.FiniteSet) or len(list(result)) > 1:
            raise AssertionError("linsolve failed")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script will run the `sympy.linsolve` function with different values of `i` and check if the results are finite sets containing only one element. If any of these conditions fail, it will raise an `AssertionError`, print the stack trace, and exit with code 1.