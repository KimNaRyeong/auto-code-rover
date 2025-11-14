Below is a Python script `reproducer.py` designed to reproduce the issue described. It will run a matrix simplification and expansion operation as per the given example, aiming to trigger the `AssertionError` when the problem is present, based on the expected behavior vs. the actual output. Remember, this requires the `sympy` library to be installed in your environment.

```python
from sympy import MatrixSymbol, ZeroMatrix, simplify, expand
from sympy.abc import m, n

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

def check_matrix_simplification():
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    Z = ZeroMatrix(m, n)

    expr_original = -(-A + B) - A + B
    
    expr_simplified = simplify(expr_original)
    expr_expanded = expand(expr_original)
    expr_zero_simplified = simplify(-(-A + B) - A + B - Z)
    expr_zero_expanded = expand(-(-A + B) - A + B - Z)
    
    # The simplified or expanded form should not match the verbose input
    # when the issue is fixed, thus triggering an assertion error when not fixed.
    try:
        assert str(expr_simplified) != "-(-A + B) -A + B", "Simplification doesn't work as expected."
        assert str(expr_expanded) != "-B + A -A + B", "Expansion doesn't work as expected."
        assert str(expr_zero_simplified) != "-(-A + B) -A + B", "Simplification with zero doesn't work as expected."
        assert str(expr_zero_expanded) != "-B + A -A + B", "Expansion with zero doesn't work as expected."
        print("Issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Non-zero to indicate a failure in reproducing the expected behavior

if __name__ == "__main__":
    try:
        check_matrix_simplification()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)  # Zero exit code to indicate success
```

To execute this, place `reproducer.py` in the root directory of your project, install `sympy` if you haven’t already (`pip install sympy`), and run `python3 reproducer.py`. The assertion errors will occur if the issue is present, printing a stack trace that gives details about where and how the failure happened.