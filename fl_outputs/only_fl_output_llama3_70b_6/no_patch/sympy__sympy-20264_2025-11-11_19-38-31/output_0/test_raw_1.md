Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp

def test_latex(expr):
    try:
        latex_expr = sp.latex(expr)
        print(f"Latex expression: {latex_expr}")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An error occurred while converting SymPy expression to LaTeX"

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

# Test cases
test_latex(sp.Pow(sp.Rational(1, 2), -1, evaluate=False))
test_latex(sp.Pow(sp.Rational(-1, -5), -1, evaluate=False))

print("All test cases passed!")
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.