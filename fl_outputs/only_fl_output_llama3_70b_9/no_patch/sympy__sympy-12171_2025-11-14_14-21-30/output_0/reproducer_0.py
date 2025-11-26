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

t = sp.symbols('t')
f = sp.Function('f')

# Test Derivative printing
expr1 = sp.Derivative(f(t), t)
printer = MCodePrinter()
result1 = printer.doprint(expr1)
assert result1 == "D[f[t], t]", f"Expected 'D[f[t], t]' but got '{result1}'"
print("Derivative test passed")

# Test Float printing
expr2 = 1.0e-4
printer = MCodePrinter()
result2 = printer.doprint(expr2)
assert result2 == "1.0*^-4", f"Expected '1.0*^-4' but got '{result2}'"
print("Float test passed")

try:
    # Run the tests
    expr1_test()
    expr2_test()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
