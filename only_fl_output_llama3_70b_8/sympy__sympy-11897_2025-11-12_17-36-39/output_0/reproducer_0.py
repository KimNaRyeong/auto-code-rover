import sympy as sp

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

x = sp.symbols('x', positive=True)

latex_output = sp.latex(sp.exp(-x)*sp.log(x))
pprint_output = str(sp.pprint(sp.exp(-x)*sp.log(x)))

if latex_output != pprint_output:
    raise AssertionError(f"LaTeX printer inconsistent with pretty printer: LaTeX={latex_output}, Pretty={pprint_output}")

x, y = sp.symbols('x y')

latex_output = sp.latex(1/(x + y)/2)
pprint_output = str(sp.pprint(1/(x + y)/2))

if latex_output != pprint_output:
    raise AssertionError(f"LaTeX printer inconsistent with pretty printer: LaTeX={latex_output}, Pretty={pprint_output}")

print("Issue not present, exiting with code 0")
sys.exit(0)
