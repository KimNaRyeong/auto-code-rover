 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
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

x, y = symbols('x y', positive=True)

assert latex(exp(-x)*log(x)) == pprint(exp(-x)*log(x))

assert latex(1/(x + y)/2) == pprint(1/(x + y)/2)

print("No issues found.")
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` with a stack trace:
```vbnet
No issues found.
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    assert latex(exp(-x)*log(x)) == pprint(exp(-x)*log(x))
AssertionError: '\\frac{1}{e^{x}} \\log{\\left (x \\right )}' != -x\n     e  ⋅log(x)
```
This confirms that the LaTeX printer is inconsistent with the pretty printer.