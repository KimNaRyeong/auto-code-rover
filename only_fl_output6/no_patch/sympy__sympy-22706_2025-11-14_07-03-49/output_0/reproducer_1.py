# reproducer.py
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

def test_issue():
    from sympy import Mul, Pow, symbols

    x = symbols('x')
    try:
        # Attempt the operation that is expected to trigger the IndexError
        result = print(Mul(Pow(x, -2, evaluate=False), Pow(3, -1, evaluate=False), evaluate=False))
        # If the operation succeeds without errors, it implies the issue is fixed.
        print("Issue not present")
        exit(0)
    except IndexError as e: # Catching the specific exception
        print_stacktrace(e)
        # The script exits with a non-zero exit code if the assertion fails.
        raise AssertionError("Issue present") from e

if __name__ == "__main__":
    test_issue()
