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
    I = sp.I
    pi = sp.pi

    expr = sp.exp(9*I*pi/4)
    assert sp.simplify(expr) != expr, "exp doesn't simplify based on its periodicity"
    
    a = expr - sp.exp(I*pi/4)
    assert sp.simplify(a) != 0, "exp doesn't simplify based on its periodicity"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

