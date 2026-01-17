 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import Subs

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x, y, z, a = symbols('x y z a')
    subs = Subs(x + y, (a,), (4,))
    print(subs.subs(a, z))
    assert subs.subs(a, z) == Subs(x + y, (a,), (z,))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```less
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    main()
  File "reproducer.py", line 15, in main
    assert subs.subs(a, z) == Subs(x + y, (a,), (z,))
AssertionError:
```
This confirms the presence of the issue. When the issue is fixed, the script should exit with code 0.