Below is a Python script named `reproducer.py` that is designed to reproduce the issue as described. It checks if the LaTeX representation of a product of a matrix symbol `x` and its negated version `-y` correctly includes necessary parentheses around `-y`. If not, it raises an `AssertionError` to indicate the presence of the issue. This script also uses the function `print_stacktrace` to print the stack trace if an exception is caught, making it easier to identify where the issue occurs.

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

def main():
    from sympy import MatrixSymbol, latex
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    latex_str = latex(expr)
    try:
        # Check if the LaTeX string correctly represents the product with necessary parentheses
        # The expected output should be 'x \\left(- y\\right)' or contain similar parentheses around '- y'
        assert "(- y)" in latex_str or "\\left(- y\\right)" in latex_str, "LaTeX printer omits necessary parentheses"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        # Exit with non-zero code to indicate issue presence
        # This line is unnecessary as the exception already indicates a failure,
        # but is added for explicitness in the script behavior
        exit(1)
    # If no exception was raised, exit with code 0 indicating the issue was not found (or is fixed)
    exit(0)
```

When you run `python3 reproducer.py` in your project's root directory, the script will work as follows:

- It attempts to reproduce the issue by generating a LaTeX string representation of the matrix product `x * (-y)`.
- If the generated LaTeX string lacks necessary parentheses around `-y`, indicating the issue is present, it asserts an error.
- If an `AssertionError` is caught, it prints the stack trace with line numbers and the code context where the error occurred.
- The script exits with code 0 if the issue is fixed (i.e., when the assertion does not fail), indicating that the issue is no longer present.