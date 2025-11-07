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
    x,y = sympy.symbols('x, y')
    result1 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)], (x, y))
    result2 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)], (x, y))
    result3 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)], (x, y))

    if not isinstance(result1, sympy.sets.FiniteSet) or len(list(result1)) > 1:
        raise AssertionError("linsolve failed")
    if not isinstance(result2, sympy.sets.FiniteSet) or len(list(result2)) > 1:
        raise AssertionError("linsolve failed")
    if not isinstance(result3, sympy.sets.FiniteSet) or len(list(result3)) > 1:
        raise AssertionError("linsolve failed")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script will run the `sympy.linsolve` function with three different values of `i` and check if the results are finite sets containing only one element. If any of these conditions fail, it will raise an `AssertionError`, print the stack trace, and exit with code 1.