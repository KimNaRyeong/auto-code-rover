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
        expr = sp.Derivative(sp.Function('f'), sp.Symbol('t'))
        printer.doprint(expr)
        assert False, "Expected error"
    except Exception as e:
        print_stacktrace(e)
        exit(1)

reproduce_issue()
