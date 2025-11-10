from sympy import symbols, Function, Derivative
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

t = symbols('t')
f = Function('f')

# Test Derivative
expr = Derivative(f(t), t)
printer = MCodePrinter()
result = printer.doprint(expr)
assert result == "D[f[t], t]", f"Expected 'D[f[t], t]' but got '{result}'"
print("Derivative test passed")

# Test Float with exponent
expr = 1.0e-4
printer = MCodePrinter()
result = printer.doprint(expr)
assert result == "1.0*^-4", f"Expected '1.0*^-4' but got '{result}'"
print("Float with exponent test passed")

print("All tests passed")
