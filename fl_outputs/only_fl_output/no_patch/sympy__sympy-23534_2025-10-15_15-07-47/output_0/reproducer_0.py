import sympy as smp

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

def check_issue():
    try:
        # Attempt to create symbols intended as instances of Function.
        q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
        # Check whether q[0] is of the expected type.
        assert type(q[0]) == smp.core.function.UndefinedFunction, "Issue found: q[0] is not of type UndefinedFunction"
    except AssertionError as e:
        # If AssertionError is caught, print the stack trace and re-raise the error.
        print_stacktrace(e)
        # Exit with a non-zero code to indicate an error state.
        raise SystemExit(1) from e

if __name__ == '__main__':
    check_issue()
    # If no exception was raised, exit with code 0 indicating success.
    print('No issue detected.')
    exit(0)
