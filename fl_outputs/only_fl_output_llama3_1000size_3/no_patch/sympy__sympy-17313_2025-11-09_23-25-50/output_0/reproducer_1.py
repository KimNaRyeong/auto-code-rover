import math
from functools import wraps

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

def assert_ceiling_and_floor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not (math.ceil(-1) > 0 and math.floor(-1) < 0 and math.ceil(1) >= 0 and math.floor(1) >= 0):
            raise AssertionError
        return result
    return wrapper

@assert_ceiling_and_floor
def test_ceiling_and_floor():
    pass

if __name__ == "__main__":
    try:
        test_ceiling_and_floor()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("No issue found.")
        exit(0)
