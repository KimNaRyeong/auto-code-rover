import sympy as sp

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

def julia_code_test():
    x, y, A = sp.symbols('x y A')
    expr = x**2*y*A**3
    julia_code = sp.printing.julia_code(expr)
    expected_julia_code = "(x .^ 2 .* y) * A ^ 3"
    if julia_code != expected_julia_code:
        print_stacktrace(AssertionError("julia_code generates invalid Julia code"))
        raise AssertionError("julia_code generates invalid Julia code")

if __name__ == "__main__":
    julia_code_test()
