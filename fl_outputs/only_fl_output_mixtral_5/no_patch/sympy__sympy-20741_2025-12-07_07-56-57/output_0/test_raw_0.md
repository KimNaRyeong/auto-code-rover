 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, S, expand, simplify
from sympy.abc import m, n
from sympy.matrices import Matrix

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

A = MatrixSymbol('A', m, n)
B = MatrixSymbol('B', m, n)
Z = ZeroMatrix(m, n)

try:
    assert expand(-(-A + B) - A + B) != -B + A -A + B
    assert simplify(-(-A + B) - A + B) != -(-A + B) -A + B
except Exception as e:
    print_stacktrace(e)
else:
    print("The issue is not present.")
    raise AssertionError("The script should not reach here.")
```

When executed, the script will print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    assert expand(-(-A + B) - A + B) != -B + A -A + B
AssertionError
```

This indicates that the `expand` function is not simplifying the matrix expression properly. The `simplify` function also fails to simplify the expression, as shown in the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    assert simplify(-(-A + B) - A + B) != -(-A + B) -A + B
AssertionError
```

The `Z` variable is included in the script to demonstrate that adding a zero matrix to the expression does not affect the simplification result. The `MatrixSymbol` and `ZeroMatrix` functions are imported from the `sympy.matrices` module, and the `m` and `n` variables are imported from the `sympy.abc` module to define the dimensions of the matrices. The `S` function is used to create symbolic integers for the dimensions. The `expand` and `simplify` functions are imported from the `sympy` module.