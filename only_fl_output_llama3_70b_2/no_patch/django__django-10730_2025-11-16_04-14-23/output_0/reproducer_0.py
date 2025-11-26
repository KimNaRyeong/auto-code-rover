import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class WrapperException(Exception):
    pass

def raise_cause():
    try:
        raise ValueError("Original exception")
    except ValueError as e:
        raise WrapperException("Wrapped exception") from e

try:
    raise_cause()
except Exception as exc:
    while True:
        if not hasattr(exc, "__cause__"):
            break
        exc = exc.__cause__
    assert False, "Infinite loop detected"
