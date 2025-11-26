Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from sympy import *

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = MatrixSymbol('x', 2, 2)
y = MatrixSymbol('y', 2, 2)
expr = (x*(-y))

try:
    latex_str = latex(expr)
    assert '(' in latex_str and ')' in latex_str, "LaTeX printer omits necessary parentheses"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
```
This script will raise an `AssertionError` if the LaTeX printer omits the necessary parentheses, and print a stack trace of the issue. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.