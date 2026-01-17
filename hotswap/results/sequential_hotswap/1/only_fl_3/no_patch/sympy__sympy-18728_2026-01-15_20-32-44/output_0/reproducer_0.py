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

def test_is_zero_and_is_positive_for_pow():
    from sympy import symbols, oo

    a, b = symbols('a b', positive=True)
    # Test cases based on the issue description
    try:
        # Case 1: Asserting (a**b).is_zero doesn't incorrectly assume False
        assert (a**b).is_zero is None, "(a**b).is_zero should be None when a or b could be infinite"

        # Case 2: Asserting (a**b).is_positive doesn't incorrectly assume True
        assert (a**b).is_positive is None, "(a**b).is_positive should be None when a or b could be infinite"

        # Case 3: Fixed scenario from the issue #9532
        n = symbols('n', real=True, finite=True)
        assert (oo / n).is_finite is False, "oo / n should not be finite when n is finite"

        # Additional case that was problematic before the fix
        n = symbols('n', finite=True)
        assert (oo / n).is_finite is False, "oo / n should not be finite when n is finite"
        
        print("All tests passed. The issue seems to be fixed.")
    
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_is_zero_and_is_positive_for_pow()
