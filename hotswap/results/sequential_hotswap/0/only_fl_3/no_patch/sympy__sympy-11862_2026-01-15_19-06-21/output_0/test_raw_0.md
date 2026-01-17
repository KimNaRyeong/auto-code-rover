Below is a Python script named `reproducer.py` that aims to reproduce the issue involving `lambdify` and precision loss with `mpmath` module when handling high-precision `Floats` from SymPy. The script raises an `AssertionError` if the issue is present, showing a clear stack trace for debugging purposes, and exits with code 0 if the issue is not observed.

```python
import sys
from sympy import symbols, sqrt, lambdify, N

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_lambdify_precision():
    x = symbols('x')
    g = sqrt(2) - x
    h = g.evalf(64)  # High-precision Float

    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')

    # Test values
    test_val = N(sqrt(2), 64)

    # Evaluate functions
    result_f1 = f1(test_val)
    result_f2 = f2(test_val)

    try:
        # Assert equality within high precision
        assert str(result_f1) == str(result_f2), "Precision loss detected between f1 and f2"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code indicating issue present

    print("No precision loss detected between f1 and f2. Issue not reproduced.")
    sys.exit(0)  # Exit with code 0 indicating issue not observed

if __name__ == "__main__":
    test_lambdify_precision()
```

This script defines a function, `test_lambdify_precision`, which constructs two symbolic expressions `g` and `h`, with `h` being a 64-digit accurate representation of `g`. It then lambdifies both expressions with `mpmath` as the module and evaluates them at a high-precision value of `sqrt(2)`. If the results from both lambdified functions differ, indicating a loss of precision, it raises an `AssertionError` and invokes the `print_stacktrace` function to provide insights into the error's origin.

To run this script, place it in the root directory of the project and execute it with Python 3. You should observe an `AssertionError` with an appropriate stack trace if the issue persists, aiding in diagnosing and ultimately resolving the problem.