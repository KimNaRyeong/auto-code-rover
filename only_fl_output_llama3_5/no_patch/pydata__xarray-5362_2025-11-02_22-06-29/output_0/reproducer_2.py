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
    import numpy as np
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error not raised"

if __name__ == "__main__":
    try:
        np.unicode_
    except AttributeError as e:
        print_stacktrace(e)
        assert False, "Expected error not raised"
