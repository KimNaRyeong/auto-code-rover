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
    try:
        x = sp.symbols('x')
        print(sp.Mul(sp.Pow(x, -2, evaluate=False), sp.Pow(3, -1, evaluate=False), evaluate=False))
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue not fixed"

if __name__ == "__main__":
    reproduce_issue()
