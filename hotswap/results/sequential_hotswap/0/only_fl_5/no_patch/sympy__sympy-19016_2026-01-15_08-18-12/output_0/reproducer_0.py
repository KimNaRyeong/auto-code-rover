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

def test_is_finite_set_property():
    from sympy import Range

    try:
        assert hasattr(Range(5), "is_finite_set"), "is_finite_set property not present in Range"
        is_finite = Range(5).is_finite_set
        assert is_finite is not None, "Range(5).is_finite_set returns None instead of a boolean"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def test_sup_inf_with_symbolic_range():
    from sympy import Symbol, oo, Range

    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        sup = s.sup  # This should raise an exception based on the reported issue.
    except Exception as e:
        # Expected failure due to unhandled Range with symbolic end.
        print("Expected failure for s.sup with symbolic range:", end=" ")
        print_stacktrace(e)
    else:
        # If no exception, this is unexpected based on the reported issue
        assert False, "Expected an error for s.sup with a symbolic range but none occurred"

def main():
    test_is_finite_set_property()
    test_sup_inf_with_symbolic_range()
    print("All tests passed successfully.")

if __name__ == "__main__":
    main()
