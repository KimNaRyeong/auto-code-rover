import sys
import traceback

class WrapperException(Exception):
    def __init__(self, exc_value=None):
        super().__init__()
        self.exc_value = exc_value

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    try:
        raise WrapperException(ValueError("test"))
    except WrapperException as exc:
        raise exc.__cause__
except Exception as e:
    print_stacktrace(e)
    assert False, "Infinite loop detected"

sys.exit(0)
