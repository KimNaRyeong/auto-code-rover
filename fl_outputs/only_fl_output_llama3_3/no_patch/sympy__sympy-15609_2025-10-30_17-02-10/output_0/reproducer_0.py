import sympy as sp
from sympy.printing import latex
from sympy.printing.latex import LatexPrinter
from io import StringIO
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

def reproduce_issue():
    i, j, k = sp.symbols("i j k")
    M = sp.MatrixSymbol("M", k, k)
    N = sp.MatrixSymbol("N", k, k)
    printer = LatexPrinter()
    stream = StringIO()
    try:
        latex((M*N)[i, j], printer=printer).encode('utf-8')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
