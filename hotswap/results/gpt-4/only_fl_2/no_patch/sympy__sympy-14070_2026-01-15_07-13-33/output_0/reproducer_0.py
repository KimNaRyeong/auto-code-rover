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

def test_logcombine():
    result = sp.logcombine(sp.log(3) - sp.log(2))
    expected_result = sp.log(3/2)
    try:
        assert sp.simplify(result - expected_result) == 0, "logcombine(log(3) - log(2)) did not simplify to log(3/2)"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_logcombine()
    except AssertionError:
        exit(1)  # Exit with error code 1 if the assertion fails
    print("Issue not present, test passed.")
    exit(0)
