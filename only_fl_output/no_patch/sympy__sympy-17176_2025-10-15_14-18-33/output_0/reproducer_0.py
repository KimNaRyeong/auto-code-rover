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

def test_bool_map_xor_to_xnor():
    from sympy import symbols, Xor, bool_map
    A1, A2, A3 = symbols('A1 A2 A3')
    f1 = Xor(A1, A2, A3)
    f2 = ~(Xor(A1, A2, A3))
    result = bool_map(f1, f2)
    expected = ((A1 & A2 & A3) | (A1 & ~A2 & ~A3) | (A2 & ~A1 & ~A3) | (A3 & ~A1 & ~A2), {A1: A1, A3: A3, A2: A2})
    assert result == expected, "bool_map does not match the expected result for XOR to XNOR conversion."

def test_finger_print_routine():
    from sympy import symbols, And, Or, Not
    from sympy.logic.boolalg import _finger
    A1, A2, A3 = symbols('A1 A2 A3')
    a = _finger(Or(And(A1, A2, A3), And(Not(A1), Not(A2), A3), And(A1, Not(A2), Not(A3)), And(Not(A1), A2, Not(A3))))
    b = _finger(Or(And(A1, A2, Not(A3)), And(Not(A1), Not(A2), Not(A3)), And(A1, Not(A2), A3), And(Not(A1), A2, A3)))
    assert a != b, "Fingerprint routine produces identical fingerprints for distinct expressions."

def main():
    try:
        test_bool_map_xor_to_xnor()
        print("bool_map XOR to XNOR test passed.")
        test_finger_print_routine()
        print("Fingerprint routine test passed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
