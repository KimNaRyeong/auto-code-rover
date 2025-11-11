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

def reproduce_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Rational calc value error not reproduced")
    return wrapper

@reproduce_issue
def test_rational_calc_value_error():
    result1 = sympy.Rational('0.5', '100')
    result2 = sympy.Rational(0.5, 100)
    assert str(result1) == "1/200" and str(result2) == "1/200"

if __name__ == "__main__":
    test_rational_calc_value_error()
    if True:
        sys.exit(0)
