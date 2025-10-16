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

def test_bool_map_xor_vs_xnr():
    from sympy import symbols, Xor, bool_map

    A1, A2, A3 = symbols('A1,A2,A3')
    f1 = Xor(A1, A2, A3)
    f2 = ~(Xor(A1, A2, A3))

    # This should not directly map as equivalent due to the negation in f2.
    try:
        result = bool_map(f1, f2)
        assert result is not None, "Expected XOR and XNR functions not to map directly as equivalent."
    except AssertionError as e:
        print_stacktrace(e)
        raise

def test_finger_function():
    from sympy import symbols
    from sympy.logic.boolalg import _finger
    from pprint import pprint

    A1, A2, A3 = symbols('A1,A2,A3')
    a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
    b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))

    # Fingerprint a and b should not be the same since the expressions are logically different.
    try:
        assert a != b, "Expected different fingerprints for logically different expressions."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_bool_map_xor_vs_xnr()
        test_finger_function()
    except AssertionError:
        exit(1)  # Exit with code 1 when the issue is present
    else:
        print("No issues detected.")  # Exit with code 0 when the issue is fixed
        exit(0)
