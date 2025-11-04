import sympy as sp
from sympy.printing import pprint, latex
import sys
import traceback

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

def main():
    try:
        sp.init_printing(use_latex=True)
        x = sp.symbols('x', positive=True)
        y = sp.symbols('y')
        
        assert latex(sp.exp(-x)*sp.log(x)) == pprint(sp.exp(-x)*sp.log(x)), "LaTeX printer inconsistent with pretty printer"
        
        assert latex(1/(x + y)/2) == pprint(1/(x + y)/2), "LaTeX printer inconsistent with pretty printer"

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
