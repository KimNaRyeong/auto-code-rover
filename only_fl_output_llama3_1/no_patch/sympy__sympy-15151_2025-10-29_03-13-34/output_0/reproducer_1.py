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

def reproduce_issue():
    x1 = sp.symbols('x_{1, i}')
    try:
        indexed_x1_i = sp.latex(x1)
        assert "x_{1,i}" in indexed_x1_i
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
