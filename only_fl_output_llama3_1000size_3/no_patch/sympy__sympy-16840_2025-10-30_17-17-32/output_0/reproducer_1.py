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
    from math import S as s
    result = s(2) // s(.5)
    assert result == 4, "Expected 4 but got {}".format(result)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Failed to reproduce the issue")
else:
    print("Issue not reproduced. Exiting with code 0.")
    sys.exit(0)
