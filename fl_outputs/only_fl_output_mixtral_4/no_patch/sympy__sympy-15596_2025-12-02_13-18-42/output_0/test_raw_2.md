 I apologize for the error in my previous response. Here is a corrected version of the standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import Poly, Rational
from sympy.abc import x

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

def degree(f, x):
    """Compute the degree of a polynomial or a rational function."""
    if not f.is_Polynomial or not f.is_ rational:
        raise ValueError("f must be a polynomial or a rational function.")
    return f.degree(x)

def main():
    f = Rational((x - 2), (x ** 2 + 1))
    expected_degree = 1
    actual_degree = degree(f, x)
    assert actual_degree == expected_degree, (
        f"Expected degree({expected_degree}) but got degree({actual_degree})."
    )

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace that shows the line numbers of the statements. The script should also exit with code 1.

If the issue is fixed, the script should exit with code 0 and print no error messages.

I apologize for any confusion caused by my previous response.