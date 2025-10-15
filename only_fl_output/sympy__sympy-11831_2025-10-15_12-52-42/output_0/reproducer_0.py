import sys
from sympy import symbols, sets, S

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    d = symbols("d")
    solution = sets.FiniteSet((d + 1, -d + 4, -d + 5, d))
    try:
        solution.intersect(S.Naturals0**4)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue still exists") from e
    else:
        print("Issue fixed, exiting with code 0")

if __name__ == "__main__":
    reproduce_issue()
