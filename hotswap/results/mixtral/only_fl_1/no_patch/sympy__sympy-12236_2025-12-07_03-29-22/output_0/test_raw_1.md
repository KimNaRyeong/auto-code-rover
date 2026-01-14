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
    assert result == expected_result, "The apart function does not give the expected result"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with Python 3.6.0 and Sympy 1.0, the script will raise an AssertionError and print a stack trace showing the issue.

To run the script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`.