from sympy import Interval, FiniteSet

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

def test_issue():
    obj1 = eval(str(Interval(0,1)))
    assert isinstance(obj1, Interval), f"Expected Interval instance but got {type(obj1)}"
    
    obj2 = eval(str(FiniteSet(1,2,3)))
    assert isinstance(obj2, FiniteSet), f"Expected FiniteSet instance but got {type(obj2)}"

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
