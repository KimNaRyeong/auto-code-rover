import sympy
import traceback
import sys

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = sympy.Symbol('x')
    try:
        sympy.pprint(x * sympy.DiracDelta(x, 1))
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue present"

if __name__ == "__main__":
    main()
