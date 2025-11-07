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

try:
    from sympy import exp, I, pi, simplify, expand_complex
    
    # Initial expression and its simplification
    expr1 = exp(9*I*pi/4)
    simplify_expr1 = simplify(expr1)
    
    # The expression after trying to simplify it
    difference_expr = exp(9*I*pi/4) - exp(I*pi/4)
    simplify_difference = simplify(difference_expr)
    expand_complex_difference = expand_complex(difference_expr)
    
    # Checking issues
    # Issue 1: `exp` does not simplify using its periodicity.
    assert expr1 != simplify_expr1, "Issue 1: Simplify incorrectly handles expression periodicity."
    # Issue 2: The difference does not simplify correctly to 0.
    assert simplify_difference != 0, "Issue 2: Simplify incorrectly handles the difference."
    # Issue 3: `expand_complex` does not simplify to 0 accurately.
    assert expand_complex_difference != 0, "Issue 3: Expand_complex incorrectly fails to simplify the expression to 0."
    
    # If no assertions are raised
    print("All issues are resolved; the script exits with code 0.")

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error code to indicate the issue is still present

except Exception as e:
    print("An unexpected error occurred; please check the test case and dependencies.")
    print_stacktrace(e)
    sys.exit(1)
