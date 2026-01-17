 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import Symbol, fps

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

if __name__ == "__main__":
    x = Symbol('x')
    p = fps(x ** 2)
    assert type(p) is not sympy.core.power.Pow, "fps(x**2) should not return a Pow object"
    try:
        p[0]
    except TypeError:
        pass  # expected exception
    else:
        raise AssertionError("fps(x**2)[0] should raise a TypeError")
else:
    raise AssertionError("This script should be run directly, not imported")
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    assert type(p) is not sympy.core.power.Pow, "fps(x**2) should not return a Pow object"
AssertionError: fps(x**2) should not return a Pow object
```
This stack trace shows that the issue is present, as the `fps` function returns a `Pow` object instead of a formal power series.

If the issue is fixed, the script should exit with code 0 and not print any stack trace.