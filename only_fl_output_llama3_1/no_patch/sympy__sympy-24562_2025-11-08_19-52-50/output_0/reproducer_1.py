import sympy
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

def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        if not isinstance(e, expected_exception):
            raise AssertionError("Expected exception of type {} but got {}".format(expected_exception.__name__, type(e).__name__))
        return
    raise AssertionError("Did not raise the expected exception")

def reproduce_issue():
    try:
        rational1 = sympy.Rational('0.5', '100')
        rational2 = sympy.Rational(0.5, 100)
        assert rational1 == rational2
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
