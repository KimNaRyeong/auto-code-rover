import sympy
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    x, y = sympy.symbols('x, y')
    
    for i in [0.0215, 0.0216, 0.0217]:
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, i * x)], (x, y))
        
        if str(result) != "FiniteSet((0, 0))":
            raise AssertionError("linsolve fails simple system of two equations")
    
    print("Issue not found")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
