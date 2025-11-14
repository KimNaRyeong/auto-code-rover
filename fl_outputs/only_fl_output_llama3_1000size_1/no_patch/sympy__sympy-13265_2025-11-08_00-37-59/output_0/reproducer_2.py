import sympy as sp

def reproduce_issue():
    m = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    simplified_m = sp.simplify(exp(m))
    assert "sin(1)" not in str(simplified_m), "Issue not fixed"
    if "sin(1)" in str(simplified_m):
        raise AssertionError("Issue not fixed")

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
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
