# reproducer.py
from sympy import symbols, Eq, exp, solve, idiff
from sympy.abc import x, y

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

def test_idiff_supports_eq():
    try:
        # This equation doesn't directly raise an exception, but it's included as
        # a contrast to the problematic cases.
        result = idiff(Eq(y*exp(y), x*exp(x)), y, x)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("idiff should support Eq but failed.")

def test_idiff_with_function():
    from sympy import Function
    f = Function('f')
    try:
        # This should ideally work and not raise an exception.
        idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
        raise AssertionError("idiff should not have supported f(x) in this context but it did.")
    except ValueError as e:
        # If the issue exists, this particular error is expected;
        # therefore do not raise an exception in this block.
        pass
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("idiff raised an unexpected exception.")

def test_idiff_without_eq_or_function():
    try:
        result = idiff(y*exp(y) - x*exp(x), y, x)
        # If no exception occurs, the bug is considered fixed for this case.
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("idiff should work without Eq or explicit function but failed.")

def main():
    test_idiff_supports_eq()
    test_idiff_with_function()
    test_idiff_without_eq_or_function()

if __name__ == "__main__":
    main()

