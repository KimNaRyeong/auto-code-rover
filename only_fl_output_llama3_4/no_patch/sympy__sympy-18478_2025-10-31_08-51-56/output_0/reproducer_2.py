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
    import sympy as sp
    x = sp.symbols('x')
    try:
        assert (sp.exp(x) + sp.cos(x)).subs(x, sp.oo) != sp.AccumBounds
        if (x + sp.cos(x)).subs(x, sp.oo) == sp.oo:
            raise AssertionError("Expected (x+cos(x)).subs(x, oo) to not be oo")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
