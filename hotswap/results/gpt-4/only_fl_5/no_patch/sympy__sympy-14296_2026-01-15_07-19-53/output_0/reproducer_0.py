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
    from sympy import sqrt, to_number_field, minimal_polynomial

    b = 1 - sqrt(2)
    a = to_number_field(b)
    
    # checking if the generated AlgebraicNumber is as expected
    assert str(a) == "-1 + sqrt(2)", "Generated AlgebraicNumber does not match expectation"

    # checking if minimal polynomial of 'b' is as expected
    assert minimal_polynomial(b).as_expr() == a.minpoly.as_expr(), "minimal polynomial of 'b' does not match a.minpoly"

    # checking if minimal polynomial of 'a' matches the expectation
    correct_minpoly_a = minimal_polynomial(-1 + sqrt(2))
    assert a.minpoly.as_expr() == correct_minpoly_a.as_expr(), "minimal polynomial of 'a' does not match the correct minimal polynomial"

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # exit with non-zero to indicate the issue is present
    else:
        print("Issue is fixed.")
        exit(0)
