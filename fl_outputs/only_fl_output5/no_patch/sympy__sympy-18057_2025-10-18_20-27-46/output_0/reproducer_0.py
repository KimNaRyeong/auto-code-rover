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

def test_sympy_comparison_with_str_repr():
    class C:
        def __repr__(self):
            return 'x.y'
    try:
        # This should not raise an exception, indicating that sympy's __eq__ does not eval repr
        sympy.Symbol('x') == C()
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("sympy incorrectly attempts to eval reprs in its __eq__ method") from e

    # Test for unexpected equality due to repr
    class D:
        def __repr__(self):
            return 'x'

    try:
        assert sympy.Symbol('x') != D(), "A sympy Symbol('x') is incorrectly equal to an object whose repr returns 'x'"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_sympy_comparison_with_str_repr()
    print("If no exception was raised, the issue is fixed.")
