```python
from sympy import symbols, latex, pprint, exp, log, init_printing
import io
import sys

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

def capture_pretty_print(expr):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    pprint(expr, use_unicode=True)
    sys.stdout = old_stdout
    return redirected_output.getvalue()

def check_printing_consistency():
    init_printing(use_unicode=True)
    x, y = symbols('x y', positive=True)
    expr1 = exp(-x)*log(x)
    latex_output1 = latex(expr1)
    pprint_output1 = capture_pretty_print(expr1)
    
    expr2 = 1/(x + y)/2
    latex_output2 = latex(expr2)
    pprint_output2 = capture_pretty_print(expr2)
    
    # Validate
    if '\\frac{1}{e^{x}} \\log{\\left (x \\right )}' not in latex_output1:
        raise AssertionError("Latex output for exp(-x)*log(x) is inconsistent.")
    if '\u212f^{-x} \\cdot \\log{\\left (x \\right )}' not in pprint_output1:
        raise AssertionError("Pretty print output for exp(-x)*log(x) is inconsistent.")
    if '\\frac{1}{2 x + 2 y}' not in latex_output2:
        raise AssertionError("Latex output for 1/(x + y)/2 is inconsistent.")
    if '1/(2⋅(x + y))' not in pprint_output2.replace(' ', ''):
        raise AssertionError("Pretty print output for 1/(x + y)/2 is inconsistent.")

try:
    check_printing_consistency()
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("Issue not found. Exiting with code 0.")
    sys.exit(0)
```