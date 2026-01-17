 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *
from reproducer_utils import print_stacktrace 

x = MatrixSymbol('x', 2, 2)
y = MatrixSymbol('y', 2, 2)
expr = (x * y).subs(y, -y)

expected_latex = "x \\left(- y\\right)"
actual_latex = latex(expr)

if expected_latex != actual_latex:
    e = AssertionError(f"Expected LaTeX: {expected_latex}, but got: {actual_latex}")
    print_stacktrace(e)
    raise e
```
To execute the script, use `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The `print_stacktrace` function is defined in a separate file `reproducer_utils.py` to keep the code clean and reusable.
```python
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
```
Note: The `reproducer_utils.py` file should be placed in the same directory as `reproducer.py`.