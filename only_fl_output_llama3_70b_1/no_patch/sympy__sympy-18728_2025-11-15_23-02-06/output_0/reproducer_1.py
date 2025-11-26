from sympy import symbols, Symbol, zoo

def test_is_zero():
    a, b = symbols('a b', positive=True)
    assert (a**b).is_zero is None  # should be None
    print("Test 1 passed")

    n = Symbol('n', real=True, finite=True)
    assert (zoo / n) != zoo  # should raise an exception
    print("Test 2 passed")

def test_is_positive():
    a, b = symbols('a b', positive=True)
    assert (a**b).is_positive is not True  # should be None
    print("Test 3 passed")

try:
    test_is_zero()
    test_is_positive()
except AssertionError as e:
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
    print_stacktrace(e)
    exit(1)

print("All tests passed")
exit(0)
