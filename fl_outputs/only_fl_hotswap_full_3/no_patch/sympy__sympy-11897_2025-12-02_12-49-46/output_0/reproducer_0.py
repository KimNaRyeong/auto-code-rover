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

x, y = symbols('x y')
x = var('x', positive=True)

assert latex(exp(-x)*log(x)) == pprint(exp(-x)*log(x), use_unicode=True), "LaTeX and pretty printer inconsistent for exp(-x)*log(x)"
assert latex(1/(x + y)/2) == pprint(1/(x + y)/2, use_unicode=True), "LaTeX and pretty printer inconsistent for 1/(x + y)/2"

print("No issues found")
sys.exit(0)
