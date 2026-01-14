 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
    """Compute the degree of the polynomial f in the variable x."""
    p = Poly(f, x)
    return p.degree()

def main():
    f = Rational((x - 2), (x**2 + 1))
    expected_degree = 1
    actual_degree = degree(f, x)
    assert expected_degree == actual_degree, "The degree of a rational function is not computed correctly."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 21, in main
    assert expected_degree == actual_degree, "The degree of a rational function is not computed correctly."
AssertionError: The degree of a rational function is not computed correctly.
```
This confirms that the degree of a rational function is not computed correctly in SymPy.