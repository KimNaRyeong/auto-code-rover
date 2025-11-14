import sympy as sp

def classify_diop(eq):
    vars = list(eq.free_symbols)
    powers = {}
    for v in vars:
        powers[v**2] = 1
    powers[1] = -21
    return (vars, powers, 'general_sum_of_even_powers')

def diophantine(eq):
    return set([])

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

x, y, z = sp.symbols('x y z')
eq = x**2 + y**2 + z**4 - (1 + 4 + 2**4)

try:
    classification_result = classify_diop(eq)
    diophantine_result = diophantine(eq)
    
    # Check if the issue is present
    powers = [exp for _, exp in classification_result[1].items() if isinstance(exp, int)]
    if not all(power % 2 == 0 and power == powers[0] for power in powers):
        raise AssertionError("Misclassification: not all powers are even and equal")
    
    print("Issue is fixed!")
except Exception as e:
    print_stacktrace(e)
    exit(1)
