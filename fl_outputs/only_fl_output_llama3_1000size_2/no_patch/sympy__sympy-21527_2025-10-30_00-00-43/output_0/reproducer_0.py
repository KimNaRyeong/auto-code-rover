import sympy
import traceback
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
    x, y = sympy.symbols('x, y')
    expected_result = (0, 0)
    
    for i in range(16):
        result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 + i * 1e-4 * x)], (x, y))
        
        if result != expected_result:
            raise AssertionError("linsolve fails simple system of two equations")
    
    print("Issue not found")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
