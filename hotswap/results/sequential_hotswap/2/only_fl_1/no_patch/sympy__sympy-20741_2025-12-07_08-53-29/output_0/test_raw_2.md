 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import MatrixSymbol, ZeroMatrix, simplify, expand, pprint
from sympy.matrices import Matrix
from sympy.abc import m, n
from sympy.external import import_module

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    # The issue is present in the following line
    expr = -(-A + B) - A + B

    try:
        expected_expanded = Matrix([[0]*n for _ in range(m)])
        expected_simplified = Matrix([[0]*n for _ in range(m)])

        actual_expanded = expand(expr)
        actual_simplified = simplify(expr)

        assert actual_expanded == expected_expanded
        assert actual_simplified == expected_simplified

        print("No issue found.")
    except AssertionError as e:
        print_stacktrace(e)
        import_module('sympy.interactive')
        pprint(expr, use_unicode=True)
        print("\nExpected (simplified/expanded):")
        pprint(expected_simplified, use_unicode=True)
        pprint(expected_expanded, use_unicode=True)
        print("\nActual (simplified/expanded):")
        pprint(simplify(expr), use_unicode=True)
        pprint(expand(expr), use_unicode=True)
```

This script defines the `print_stacktrace` function to print the stack trace when an `AssertionError` is raised. It then creates the matrix symbols `A`, `B`, and `Z` as described in the issue. The expression `-(-A + B) - A + B` is stored in the `expr` variable.

The script then calculates the expected simplified and expanded forms of the expression, which should both be the zero matrix. It then calculates the actual simplified and expanded forms of the expression and checks if they match the expected forms. If they don't, an `AssertionError` is raised and the stack trace is printed.

The script also prints the original expression, the expected and actual simplified and expanded forms of the expression when the `AssertionError` is raised. This allows the user to easily see the issue and compare the expected and actual forms of the expression.