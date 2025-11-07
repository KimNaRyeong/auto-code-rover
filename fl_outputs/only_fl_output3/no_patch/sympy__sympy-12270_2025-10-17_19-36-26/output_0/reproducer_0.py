from sympy import I, Mul, symbols

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

def test_extract_multiplicatively():
    # Define symbols
    x, y = symbols('x y')

    # Test cases
    try:
        assert (2 + 4*I).extract_multiplicatively(2) == 1 + 2*I, "Case 1 failed"
        assert (-2 - 4*I).extract_multiplicatively(-1) == 2 + 4*I, "Case 2 failed"
        extracted_case_3 = (-2 - 4*I).extract_multiplicatively(-2)
        assert extracted_case_3, f"Case 3 failed: {extracted_case_3}"

        assert (2*x + 4*y + 8).extract_multiplicatively(2) == x + 2*y + 4, "Case 4 failed"
        assert (-2*x - 4*y - 8).extract_multiplicatively(2) == -x - 2*y - 4, "Case 5 failed"
        assert (-2*x - 4*y - 8).extract_multiplicatively(-1) == 2*x + 4*y + 8, "Case 6 failed"
        extracted_case_7 = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert extracted_case_7, f"Case 7 failed: {extracted_case_7}"
        print("All cases passed, seems like the issue is fixed")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_extract_multiplicatively()
