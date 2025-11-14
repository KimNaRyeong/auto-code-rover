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

def main():
    I = sp.symbols('I')
    pi = sp.pi

    expr = sp.exp(9*I*pi/4)
    simplified_expr = sp.simplify(expr)

    assert simplified_expr != expr, "exp didn't simplify based on its periodicity"

    a = expr - sp.exp(I*pi/4)
    expanded_a = sp.expand_complex(a)

    assert expanded_a == 0, "expand_complex didn't reduce the expression to 0"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
