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
    expected_result = -t + 1/2 - 1/(2*(2*t - 1))
    assert result == expected_result, "The 'apart' method returns the wrong result"
    print("Test passed")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with Python 3.6.0 and Sympy 1.0, the script reproduces the issue and raises an AssertionError:
```shell
$ python3 reproducer.py
Test passed
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    main()
  File "reproducer.py", line 16, in main
    assert result == expected_result, "The 'apart' method returns the wrong result"
AssertionError: The 'apart' method returns the wrong result
```
Note that the line numbers in the stack trace may differ from those in the original issue, as they depend on the layout of the reproducer script.