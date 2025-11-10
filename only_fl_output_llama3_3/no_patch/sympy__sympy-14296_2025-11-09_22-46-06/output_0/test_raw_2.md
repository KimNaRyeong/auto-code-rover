Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

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

def main():
    b = sp.Rational(1) - sp.sqrt(sp.Rational(2))
    a = sp.to_number_field(b)
    if not (a.minpoly.as_poly().as_coeff_Mul()[0].as_expr() == sp.Poly([1, 2], sp.symbols('x'), domain='QQ')):
        raise AssertionError("Issue present")
    print_stacktrace(Exception())

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed")
        exit(0)
```

This script creates the algebraic number `b` and then calls `to_number_field` to create an `AlgebraicNumber` generating the extension field. It checks if the minimal polynomial of this generated number is correct, and if not, raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the issue.

To run the script, save it in a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.