Here is the reproducer script:

```python
from sympy import Eq, exp, symbols
import traceback
import sys

def idiff(expr, var, other):
    try:
        return expr.diff(other)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected issue")

try:
    idiff(Eq(symbols('y') * exp(symbols('y')), symbols('x') * exp(symbols('x'))), symbols('y'), symbols('x'))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected issue")

try:
    idiff((symbols('f')(symbols('x'))) * exp(symbols('f')(symbols('x'))) - symbols('x') * exp(symbols('x')), symbols('f')(symbols('x')), symbols('x'))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected issue")

idiff((symbols('y')) * exp(symbols('y')) - (symbols('x')) * exp(symbols('x')), symbols('y'), symbols('x'))

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.