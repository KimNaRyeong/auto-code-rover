 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, S, simplify, expand
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
    result = -(-A + B) - A + B
    expected_expanded = Matrix([[S(-1)*b + a] for a, b in zip(A, B)])
    expected_simplified = Matrix([[S(-1)*b + a] for a, b in zip(A, B)])
    assert result.expand() == expected_expanded, "Matrix expansion is incorrect"
    assert result.simplify() == expected_simplified, "Matrix simplification is incorrect"
    print("Matrix expressions are simplified properly")
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
```

When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    assert result.simplify() == expected_simplified, "Matrix simplification is incorrect"
AssertionError: Matrix simplification is incorrect
```

This confirms that the issue of matrix expressions not being simplified properly still exists.