# reproducer.py
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

def test_logcombine_issue():
    expr = sp.log(3) - sp.log(2)
    combined_expr = sp.logcombine(expr)
    expected_expr = sp.log(3/2)
    
    try:
        # Check if the combined expression equals the expected expression
        assert sp.simplify(combined_expr - expected_expr) == 0, "logcombine did not simplify as expected"
    except AssertionError as e:
        print_stacktrace(e)
        raise

def main():
    try:
        test_logcombine_issue()
    except AssertionError:
        # An AssertionError indicates that the issue is present
        exit(1)  # Non-zero exit code indicates failure

if __name__ == "__main__":
    main()
    print("Issue resolved.")  # This line is executed only if no assertion fails
    exit(0)  # Zero exit code indicates success
