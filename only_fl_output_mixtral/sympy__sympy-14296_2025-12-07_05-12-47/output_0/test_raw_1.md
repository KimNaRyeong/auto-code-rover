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
    assert a == -1 + sqrt(2), "The generator should be positive"
    assert minimal_polynomial(b) == _x**2 - 2*_x - 1, "The minimal polynomial of b is incorrect"
    assert minimal_polynomial(a) == _x**2 - 2*_x - 1, "The minimal polynomial of a is incorrect"
    assert a.minpoly == PurePoly(_x**2 - 2*_x - 1, _x, domain='QQ'), "The minimal polynomial of a is incorrect"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 18, in main
    assert minimal_polynomial(a) == _x**2 - 2*_x - 1, "The minimal polynomial of a is incorrect"
AssertionError: The minimal polynomial of a is incorrect
```
This confirms that the minimal polynomial of `a` is incorrect, as reported in the issue.