import sympy as sp

def classify_diop(eq):
    vars = list(eq.free_symbols)
    coeffs = {}
    for term in eq.as_coeff_add(*vars):
        if isinstance(term, sp.Pow):
            base, power = term.as_base_exp()
            coeffs[term] = 1
        else:
            coeffs[term] = 1
    return vars, coeffs, 'general_sum_of_even_powers'

def diophantine(eq):
    vars, coeffs, _ = classify_diop(eq)
    powers = set()
    for expr in coeffs.keys():
        if isinstance(expr, sp.Pow):
            base, power = expr.as_base_exp()
            powers.add(power)
    if len(set(powers)) != 1:
        raise AssertionError("All powers are not the same")
    return set()

x, y, z = sp.symbols('x y z')
eq = x**2 + y**2 + z**4 - (1+4+2**4)

try:
    diophantine(eq)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue is fixed")
    sys.exit(0)

import sys
def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
