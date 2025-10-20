def main():
    try:
        from sympy import symbols, Xor
        from sympy.logic.boolalg import _finger, bool_map
        from collections import defaultdict
        from pprint import pprint

        # Define symbols
        A1, A2, A3 = symbols('A1, A2, A3')

        # Define two functions using XOR
        f1 = Xor(A1, A2, A3)
        f2 = ~(Xor(A1, A2, A3))

        # Attempt to map f1 to f2 using bool_map
        result = bool_map(f1, f2)

        expected_result = ((A1 & A2 & A3) | (A1 & ~A2 & ~A3) | (A2 & ~A1 & ~A3) | (A3 & ~A1 & ~A2), {A1: A1, A3: A3, A2: A2})

        # Check if the result is as expected
        assert result == expected_result, "bool_map result does not match the expected result."

        # Test the _finger function to check for identical fingerprints
        a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
        b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))

        # Check if fingerprints are incorrectly identical
        assert a != b, "_finger function produces identical fingerprints for distinct expressions."

    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
