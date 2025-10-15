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

try:
    from sympy import frac, zoo
    result = frac(zoo)
    # If frac(zoo) does not throw an exception, it means the issue is fixed.
    # We assert a failure here to make sure the script behaves as expected when the issue exists.
    assert False, "frac(zoo) should have raised TypeError"
except TypeError as e:
    print_stacktrace(e)
    # Reraise the exception to make clear the script encountered the known issue.
    raise AssertionError("Known TypeError issue encountered with frac(zoo).") from e
except Exception as e:
    # If any other exception is caught, it means something else went wrong.
    print("An unexpected exception occurred.")
    print_stacktrace(e)
    raise
else:
    # If no exception is raised, it means the issue is probably fixed.
    print("Issue with frac(zoo) seems to be fixed.")
    exit(0)
