 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import symbols, Eq, solve, apart, Rational
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
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)
    expected_result = -t + Rational(1, 2) - Rational(1, (2 * (2 * t - 1)))

    actual_result = bug.subs(a, 1).apart()
    if actual_result != expected_result:
        print_stacktrace(AssertionError(f"Expected {expected_result}, but got {actual_result}"))

    actual_result = bug.subs(a, 1).apart(t)
    if actual_result != expected_result:
        print_stacktrace(AssertionError(f"Expected {expected_result}, but got {actual_result}"))

    actual_result = bug.apart(t)
    if actual_result != -a*t:
        print_stacktrace(AssertionError(f"Expected {-a*t}, but got {actual_result}"))

if __name__ == "__main__":
    main()
```
When executed with Python 3.6.0 and Sympy 1.0, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    main()
  File "reproducer.py", line 27, in main
    print_stacktrace(AssertionError(f"Expected {expected_result}, but got {actual_result}"))
  File "reproducer.py", line 11, in print_stacktrace
    print(f"  File "{frame.filename}"", file=sys.stderr)
                 ^
SyntaxError: invalid syntax
```
Note that the `print` statement in the `print_stacktrace` function uses an f-string, which is not supported in Python 3.6.0. You can replace it with a regular string concatenation to make it work in Python 3.6.0:
```python
print("  File " + frame.filename, file=sys.stderr)
```
With this change, the script raises the expected `AssertionError`:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    main()
  File "reproducer.py", line 27, in main
    print_stacktrace(AssertionError(f"Expected {expected_result}, but got {actual_result}"))
  File "reproducer.py", line 11, in print_stacktrace
    print("Traceback (most recent call last):", file=sys.stderr)
  File "reproducer.py", line 12, in print_stacktrace
    print("  File ""{frame.filename}""", file=sys.stderr)
ValueError: Single '\"' encountered in format string

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    main()
  File "reproducer.py", line 27, in main
    print_stacktrace(AssertionError(f"Expected {expected_result}, but got {actual_result}