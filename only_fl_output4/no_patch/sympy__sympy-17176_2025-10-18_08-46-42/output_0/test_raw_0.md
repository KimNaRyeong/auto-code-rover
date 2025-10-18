```python
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

def test_bool_map_xor3_xnr3_equivalence():
    from sympy import symbols, Xor, bool_map

    A1, A2, A3 = symbols('A1 A2 A3')
    f1 = Xor(A1, A2, A3)
    f2 = ~(Xor(A1, A2, A3))
    result = bool_map(f1, f2)

    # Expecting the result to be not equal due to the issue.
    expected_result = not f1.equals(f2)
    assert result == expected_result, "Bool_map does not correctly find the equivalence for xor3 and xnr3."

def test_finger_function_for_xor():
    from sympy import symbols
    from sympy.logic.boolalg import _finger
    from collections import defaultdict

    A1, A2, A3 = symbols('A1 A2 A3')
    a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
    b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
    
    # Expecting a and b to have different fingerprints due to the difference in logic operations
    assert a != b, "Fingerprint function produces identical outputs for different logic operations."

try:
    test_bool_map_xor3_xnr3_equivalence()
    test_finger_function_for_xor()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with error code if assertion fails
else:
    print("All tests passed successfully!")
    exit(0)  # Exit with success code if no issue is found
```