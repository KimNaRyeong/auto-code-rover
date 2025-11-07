# reproducer.py
from sympy import pi, E, pretty, init_printing
import sys

# Ensure that symbols are rendered as strings
init_printing(use_unicode=True)

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

def verify_issue():
    expr = pi**(1/E)
    pretty_output = pretty(expr)
    incorrect_output = "-1___\n╲╱ π "

    # Check if the pretty printing of the expression matches the incorrect output
    if pretty_output == incorrect_output:
        raise AssertionError("The issue with pretty printing of pi**(1/E) is reproduced.")


def main():
    try:
        verify_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status indicating the issue is present
    
    # If the issue is not reproduced, exit with code 0
    print("The issue with pretty printing of pi**(1/E) has been resolved.")
    sys.exit(0)

if __name__ == "__main__":
    main()
