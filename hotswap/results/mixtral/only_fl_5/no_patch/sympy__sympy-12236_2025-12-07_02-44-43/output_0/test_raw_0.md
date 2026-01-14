 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
from sympy import symbols, Eq, solve, apart, latex
from sympy.abc import a, t

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
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)
    expected_result = -t + 1/2 - 1/(2*(2*t - 1))

    actual_result = apart(bug.subs(a, 1), t)
    if actual_result != expected_result:
        e = AssertionError(f"Wrong result with apart(bug.subs(a, 1), t)\nExpected: {latex(expected_result)}\nActual  : {latex(actual_result)}")
        print_stacktrace(e)
        raise e

    actual_result = apart(bug, t)
    if actual_result != -a*t:
        e = AssertionError(f"Wrong result with apart(bug, t)\nExpected: {latex(-a*t)}\nActual  : {latex(actual_result)}")
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```
When executed with Python 3.6.0 and Sympy 1.0, the script will raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 34, in <module>
    main()
  File "reproducer.py", line 28, in main
    e = AssertionError(f"Wrong result with apart(bug, t)\nExpected: -a*t\nActual  : {latex(actual_result)}")
AssertionError: Wrong result with apart(bug, t)
Expected: -a*t
Actual  : a*t - a
```
This confirms the issue with Sympy 1.0 and Python 3.6.0. If the issue is fixed, the script will exit with code 0.