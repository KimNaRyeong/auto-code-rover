import sympy as sp

def main():
    # Create a matrix expression
    expr = sp.exp(sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))

    # Simplify the expression
    simplified_expr = sp.simplify(expr)

    # Check if sin(1) is recognized
    expected_expr = sp.Matrix([[sp.cos(1), -sp.sin(1), 0], [0, sp.cos(1), 0], [0, 0, 1]])
    assert simplified_expr == expected_expr, "sin(1) not recognized"

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

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
