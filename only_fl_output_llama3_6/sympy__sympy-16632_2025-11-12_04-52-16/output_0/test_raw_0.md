Here is the reproducer script:

```python
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                         implicit_multiplication_application)

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
    transformations = (standard_transformations + (implicit_multiplication_application,))
    expr1 = parse_expr('2**n * 3**n')
    expr2 = parse_expr('2**n3**n', transformations=transformations)
    
    print(type(expr1), expr1.args, expr1)  # <class 'sympy.core.power.Pow'> (6, n) 6**n
    print(type(expr2), expr2.args, expr2)  # <class 'sympy.core.mul.Mul'> (3**n, 2**n) 3**n*2**n
    
    result = expr1 - expr2
    assert result == sp.S.Zero, "Expected 0 but got {}".format(result)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will simply exit with code 0.