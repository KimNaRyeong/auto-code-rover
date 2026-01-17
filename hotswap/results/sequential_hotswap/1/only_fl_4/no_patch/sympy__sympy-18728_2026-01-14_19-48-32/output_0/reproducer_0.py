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

def test_pow_behavior():
    from sympy import symbols, oo

    a, b = symbols('a b', positive=True)
    
    # Test cases based on the issue description
    try:
        # Case 1: a**b should not definitively be non-zero when a or b could be infinite
        assert (a**b).is_zero == None, "(a**b).is_zero should be None when a or b could be infinite"

        # Case 2: a**b should not definitively be positive when it could be zero
        assert (a**b).is_positive == None, "(a**b).is_positive should be None when a or b could be infinite"
        
        # Additional case based on issue #9532
        n = symbols('n', real=True, finite=True)
        assert (oo / n).is_finite == False, "oo / n should be considered infinite"

        # Checking for the problematic case where the assumptions weren't handling infinity well
        n = symbols('n', finite=True)
        assert (oo / n).is_finite == None, "oo / n should not simplistically be regarded as finite or infinite"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_pow_behavior()
    print("All tests passed. The issue seems to have been fixed.")
