Here is the reproducer script:

```python
import sympy as sp
from assertpy import assert_that

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
    sympy_version = sp.__version__
    if sympy_version == '1.5.1':
        expr = sp.sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
        result = expr.simplify()
        assert_that(result).is_equal_to(4*sp.ceiling(x/4) - 3)
    elif sympy_version == '1.6.2':
        expr = sp.sympify('4*ceiling(x/4 - 3/4)', evaluate=False)
        result = expr.simplify()
        assert_that(result).is_equal_to(4*sp.ceiling(x/4) - 3)
    else:
        print("Sympy version not supported")
        return

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue reproduced successfully. Sympy version is not affected.")
    exit(0)
```

This script checks the version of sympy and then tries to reproduce the issue by asserting that the result of `simplify` for a given expression is equal to the expected value. If the assertion fails, it prints the stack trace and exits with code 1.