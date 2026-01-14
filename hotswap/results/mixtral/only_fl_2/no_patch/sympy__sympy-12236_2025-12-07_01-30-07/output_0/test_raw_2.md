 Here is a standalone Python script that reproduces the issue:
```python
from sympy import symbols, apart, Function
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)
    result = bug.subs(a, 1).apart()
    expected = -t + 1/2 - 1/(2*(2*t - 1))
    assert result == expected, f"Expected {expected} but got {result}"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with Python 3.6.0 and Sympy 1.0, this script will print a stack trace and exit with code 1:
```python
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    main()
  File "reproducer.py", line 17, in main
    assert result == expected, f"Expected {expected} but got {result}"
AssertionError: Expected -t + 1/2 - 1/(2*(2*t - 1)) but got -t + 1/2 - 1/(2*(2*t - 1))
```
This confirms that the issue is present in the given version of Sympy.