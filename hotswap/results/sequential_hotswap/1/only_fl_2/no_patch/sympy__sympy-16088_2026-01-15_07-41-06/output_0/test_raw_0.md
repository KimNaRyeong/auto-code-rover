Below is the standalone Python file `reproducer.py` designed to reproduce the issue described. This script will raise an `AssertionError` if the issue is present, showing a detailed stack trace for better debugging. Conversely, if the issue has been fixed, it will exit with code 0 without any error.

```python
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

def test_issue():
    from sympy import Integral, Sum, symbols, simplify

    x, y, z, n = symbols('x y z n')
    integral_simplified = simplify(Integral(x*y - z, x))
    sum_simplified = simplify(Sum(x*y, (x, 1, n)))

    try:
        assert integral_simplified == y*Integral(x, x) - z*Integral(1, x), "Integral does not simplify correctly"
        assert str(sum_simplified) == "y*Sum(x, (x, 1, n))", "Sum does not simplify correctly"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_issue()
```

This script leverages SymPy's `simplify` function on both `Integral` and `Sum` objects with the expectation that constant terms outside the integrand (for `Integral`) and the summation (for `Sum`) will be correctly factored out. The success of these operations is asserted against the expected outcomes, capturing a scenario where either operation might not behave as intended.

If the `simplify` function works as described in the issue assertion, both assertions will pass, and the script ends normally. Otherwise, an AssertionError is raised, and the stack trace is printed, pinpointing where the assumption failed, thus indicating the issue is still present in the environment where the script is executed.