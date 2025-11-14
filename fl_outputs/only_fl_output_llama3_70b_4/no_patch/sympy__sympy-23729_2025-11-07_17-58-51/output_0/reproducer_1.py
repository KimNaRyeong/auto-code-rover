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

def julia_code_issue():
    x, y, A = sp.symbols('x y A')
    expr = x**2*y*A**3
    julia_code = sp.printing.julia.julia_code(expr)
    try:
        assert julia_code == "(x .^ 2 .* y) * A ^ 3"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    julia_code_issue()
