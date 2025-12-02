 I apologize for the mistake in my previous response. Here is the corrected `reproducer.py` script that should reproduce the issue:
```python
from sympy import pprint, latex, var, exp, log, Rational
from sympy.abc import x, y
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

def test_issue():
    # Test case 1: inconsistent output for exp(-x)*log(x)
    x = var('x', positive=True)
    latex_output = latex(exp(-x)*log(x))
    pprint_output = pprint(exp(-x)*log(x))
    if latex_output != pprint_output:
        msg = f"LaTeX printer inconsistent with pretty printer: {latex_output} vs {pprint_output}"
        raise AssertionError(msg)

    # Test case 2: inconsistent output for 1/(x + y)/2
    x, y = var('x y')
    latex_output = latex(1/(x + y)/2)
    pprint_output = pprint(1/(x + y)/2)
    if latex_output != pprint_output:
        msg = f"LaTeX printer inconsistent with pretty printer: {latex_output} vs {pprint_output}"
        raise AssertionError(msg)

if __name__ == "__main__":
    try:
        test_issue