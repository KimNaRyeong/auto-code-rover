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

i, j, k = sp.symbols("i j k")
M = sp.MatrixSymbol("M", k, k)
N = sp.MatrixSymbol("N", k, k)

try:
    latex_str = latex((M*N)[i, j])
    assert "_" not in latex_str, "LaTeX string contains invalid subscript '_'"
    print("Issue is fixed!")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
