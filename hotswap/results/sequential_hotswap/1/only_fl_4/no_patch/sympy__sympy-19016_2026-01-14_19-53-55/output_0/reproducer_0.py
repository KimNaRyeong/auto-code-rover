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

def test_is_finite_set_implemented():
    from sympy import Range
    assert hasattr(Range(5), 'is_finite_set'), "is_finite_set property is not implemented for Range."

def test_sup_inf_with_symbolic_integer():
    from sympy import Range, Symbol, oo
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        _ = s.sup
        _ = s.inf
        # (Place for future checks if needed)
    except ValueError as e:
        print_stacktrace(e)
        assert False, "sup/inf calculation with symbolic integer and Range failed."

def main():
    try:
        test_is_finite_set_implemented()
        test_sup_inf_with_symbolic_integer()
        print("All tests passed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
