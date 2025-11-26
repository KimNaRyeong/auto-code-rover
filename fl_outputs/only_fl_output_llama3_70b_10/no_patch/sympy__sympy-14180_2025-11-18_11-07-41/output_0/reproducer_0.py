import sympy as sp
from sympy.printing.latex import latex

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

def test_latex_conversion():
    expr = sp.ln(10)
    latex_expr = latex(expr)
    assert latex_expr == r'\ln\left(10\right)', f"Expected '\\ln{{10}}', but got '{latex_expr}'"

try:
    test_latex_conversion()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
