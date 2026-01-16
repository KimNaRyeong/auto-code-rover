import sys

def simulate_django_exception_handling():
    try:
        try:
            raise RuntimeError('my error')
        except RuntimeError as e:
            new_exception = ValueError('my new error')
            raise new_exception from None  # Indicating suppression of the context
    except ValueError as final_exc:
        return final_exc

def check_exception_suppression(exc):
    """
    Mimics the logic that should respect __suppress_context__,
    to check if the context of the original exception is suppressed.
    """
    if exc.__cause__ is not None or exc.__context__ is not None:
        return False  # Means __suppress_context__ is not respected
    return True  # Means __suppress_context__ is respected

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

if __name__ == "__main__":
    exception = simulate_django_exception_handling()
    if not check_exception_suppression(exception):
        print_stacktrace(exception)
        raise AssertionError("The issue is present.")

    print("The issue is fixed.")
    sys.exit(0)
