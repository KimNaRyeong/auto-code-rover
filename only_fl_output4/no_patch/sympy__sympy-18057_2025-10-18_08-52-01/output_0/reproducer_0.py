# reproducer.py
import sympy

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

def test_sympy_eq_behavior():
    class C:
        def __repr__(self):
            return 'x.y'
    
    try:
        _ = sympy.Symbol('x') == C()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Sympy __eq__ method should not attempt to eval reprs of unknown objects") from e
    
    class D:
        def __repr__(self):
            return 'x'
    
    try:
        assert sympy.Symbol('x') != D(), "Sympy incorrectly compares equal to an object with a matching repr"
    except AssertionError as e:
        print_stacktrace(e)
        raise AssertionError("Incorrect equality result between sympy Symbol and an object with matching repr") from e

if __name__ == "__main__":
    test_sympy_eq_behavior()
