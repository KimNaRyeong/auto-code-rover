from sympy import symbols, bell, oo
import sys

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

def test_bell_limit():
    n = symbols('n')
    result = bell(n).limit(n, oo)
    try:
        assert result == oo, "The limit of bell(n) as n approaches infinity should be oo."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue fixed. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    test_bell_limit()
