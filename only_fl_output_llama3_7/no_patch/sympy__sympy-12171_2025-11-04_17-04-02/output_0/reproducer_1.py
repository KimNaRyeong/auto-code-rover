import sympy as sp
from sympy.printing.mathematica import MCodePrinter

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
    try:
        printer = MCodePrinter()
        expr1 = sp.Derivative('f(t)', 't')
        expr2 = 1.0e-4
        assert str(printer.doprint(expr1)) == "D[f[t],t]" and str(printer.doprint(expr2)).replace('e','*^') == '1.0*^-4'
    except AssertionError:
        print_stacktrace(Exception("Issue not reproduced"))
        raise
    else:
        print("Issue fixed")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
