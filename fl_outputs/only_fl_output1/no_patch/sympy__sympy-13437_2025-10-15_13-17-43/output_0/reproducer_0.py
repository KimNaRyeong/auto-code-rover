# reproducer.py
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

def main():
    from sympy import symbols, bell, oo
    n = symbols('n')

    try:
        # Check if the bell function's limit as n approaches infinity evaluates to infinity
        result = bell(n).limit(n, oo)
        assert result == oo, "bell(n).limit(n, oo) did not evaluate to oo"
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with non-zero code to indicate failure (presence of issue)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issue detected, limit evaluates correctly.")
        # Exit with code 0 to indicate the issue is fixed
        sys.exit(0)

if __name__ == "__main__":
    main()
