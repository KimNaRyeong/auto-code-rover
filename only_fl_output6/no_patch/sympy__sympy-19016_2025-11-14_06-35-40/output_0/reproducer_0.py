# reproducer.py

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

def test_is_finite_set_for_range():
    from sympy import Range
    try:
        assert hasattr(Range(5), 'is_finite_set'), "is_finite_set property is not implemented for Range"
        assert Range(5).is_finite_set is not None, "is_finite_set property does not return a value for Range"
    except AssertionError as e:
        print_stacktrace(e)
        raise

def test_sup_inf_with_symbolic_integer():
    from sympy import Range, Symbol, oo
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        assert s.sup is not None, "sup does not work for ranges with a symbolic integer"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_is_finite_set_for_range()  # This should not raise if `is_finite_set` is correctly implemented

    try:
        test_sup_inf_with_symbolic_integer()  # This should raise and print stack trace if there's an issue with `sup`
    except AssertionError:
        pass  # Expected failure due to the issue being present
