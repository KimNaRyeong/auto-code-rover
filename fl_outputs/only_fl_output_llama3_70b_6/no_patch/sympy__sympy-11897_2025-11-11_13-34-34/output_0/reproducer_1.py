from sympy import symbols, exp, log, latex, pprint
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

x = symbols('x', positive=True)

latex_output = latex(exp(-x)*log(x))
pprint_output = pprint(exp(-x)*log(x), use_unicode=True)

if latex_output != '\\frac{1}{e^{x}} \\log{\\left (x \\right )}':
    raise AssertionError(f"LaTeX output is inconsistent: {latex_output}")

x, y = symbols('x y')

latex_output = latex(1/(x + y)/2)
pprint_output = pprint(1/(x + y)/2, use_unicode=True)

if latex_output != '\\frac{1}{2 x + 2 y}':
    raise AssertionError(f"LaTeX output is inconsistent: {latex_output}")

sys.exit(0)
