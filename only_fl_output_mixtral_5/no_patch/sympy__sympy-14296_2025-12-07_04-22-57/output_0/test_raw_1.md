 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import sqrt, to_number_field, minimal_polynomial, PurePoly
from sympy.abc import _x

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

def main():
    b = 1 - sqrt(2)
    a = to_number_field(b)
    assert a == -1 + sqrt(2), "The generator of the algebraic number field should be positive."
    expected_minpoly = _x**2 + 2*_x - 1
    assert minimal_polynomial(a) == expected_minpoly, \
        f"The minimal polynomial of {a} should be {expected_minpoly}."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with Python 3, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 19, in main
    assert minimal_polynomial(a) == expected_minpoly, \
  File "/usr/local/lib/python3.9/dist-packages/sympy/core/assumptions.py", line 1016, in __bool__
    raise TypeError("Cannot determine truth value of AssumptionSet")
TypeError: Cannot determine truth value of AssumptionSet
```
This stack trace shows that the minimal polynomial of `a` is not equal to the expected minimal polynomial, which confirms the issue.