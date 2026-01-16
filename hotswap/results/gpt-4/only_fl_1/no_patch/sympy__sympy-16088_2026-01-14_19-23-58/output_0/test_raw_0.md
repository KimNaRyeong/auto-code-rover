Below is a standalone Python file named `reproducer.py` designed according to your instructions. This script will attempt to simulate the described issue. When executed, it will raise an `AssertionError` if the issue is present, along with a detailed stack trace. Once the issue is resolved, it should exit with code 0 without raising any exceptions.

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
    from sympy import symbols, Integral, Sum, simplify

    x, y, z, n = symbols('x y z n')
    integral_expr = Integral(x*y - z, x)
    simplified_integral_expr = simplify(integral_expr)
    expected_integral_result = y*Integral(x, x) - z*Integral(1, x)

    sum_expr = Sum(x*y, (x, 1, n))
    simplified_sum_expr = simplify(sum_expr)
    expected_sum_result = y*Sum(x, (x, 1, n))

    assert simplified_integral_expr == expected_integral_result, "Integral simplification failed"
    assert simplified_sum_expr == expected_sum_result, "Sum simplification failed"

def main():
    try:
        test_issue()
        print("The issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

To utilize this script:

1. Place `reproducer.py` in the root directory of the project.
2. Run it using the command: `python3 reproducer.py`.

If the issue has been resolved, the output will simply be "The issue is fixed." If not, the script will print the stack trace and indicate through an `AssertionError` that the problem persists, pointing specifically to the part of the code where the expectation is not met.