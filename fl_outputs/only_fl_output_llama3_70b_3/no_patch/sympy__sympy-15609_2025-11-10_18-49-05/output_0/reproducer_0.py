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
    if "_i_1" in latex_str:
        raise AssertionError("Indexed matrix-expression LaTeX printer is not compilable")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
