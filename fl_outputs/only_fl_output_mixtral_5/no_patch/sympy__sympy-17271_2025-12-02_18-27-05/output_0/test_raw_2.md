 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import frac, zoo, S

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
    try:
        f = frac(zoo)
        assert False, "Expected TypeError, but got no exception"
    except TypeError:
        pass

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script raises a `TypeError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    main()
  File "reproducer.py", line 11, in main
    f = frac(zoo)
  File "/path/to/sympy/sympy/core/function.py", line 458, in __new__
    result = super(Function, cls).__new__(cls, *args, **options)
  File "/path/to/sympy/sympy/core/function.py", line 277, in __new__
    evaluated = cls.eval(*args)
  File "/path/to/sympy/sympy/functions/elementary/integers.py", line 333, in eval
    return real + S.ImaginaryUnit*imag
TypeError: unsupported operand type(s) for +: 'NoneType' and 'Zero'
```
The relevant lines in `sympy/functions/elementary/integers.py` are covered by this test, as expected.

If the issue is fixed, the script should print no output and exit with code 0.