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

def test_zero_matrix_truth_value():
    from sympy import ZeroMatrix

    Z = ZeroMatrix(2, 3)
    Ze = Z.as_explicit()

    try:
        # Check the truth value of Z explicitly
        assert bool(Z) == True, "ZeroMatrix should not be falsey"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    try:
        # Verify the explicit matrix version does not raise inconsistency
        assert bool(Ze) == True, "Explicit ZeroMatrix should not be falsey"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_zero_matrix_truth_value()
