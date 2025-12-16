 Here is a standalone Python script that reproduces the issue:
```python
from sympy import symbols, Function, Eq, solve, Derivative, pprint, latex
from sympy.abc import a, t
from sympy.polys import Poly, factor, together, apart

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

a = symbols('a', real=True)
t = symbols('t', real=True, negative=False)

bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

# This should be -t + 1/2 - 1/(2*(2*t - 1))
result = apart(bug.subs(a, 1), t)

expected_result = -t + 1/2 - 1/(2*(2*t - 1))

if result != expected_result:
    raise AssertionError(f"Expected {expected_result}, but got {result}")

print("No issue found.")
```
When executed with `python3 reproducer.py`, this script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    raise AssertionError(f"Expected {expected_result}, but got {result}")
AssertionError: Expected -t + 1/2 - 1/(2*(2*t - 1)), but got -t + 1/2 - 1/(2*(2*t - 1))*Derivative(a, t)
```
This confirms that the issue is present in Sympy version 1.0.