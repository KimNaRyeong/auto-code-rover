import sympy as sp

def reproduce_issue():
    try:
        result = sp.polylog(2, sp.Rational(1, 2)).expand(func=True).evalf()
        expected_result = -sp.log(2)**2/2 + sp.pi**2/12
        if not sp.simplify(result - expected_result) == 0:
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
    reproduce_issue()
