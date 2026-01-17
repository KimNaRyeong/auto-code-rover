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

try:
    from sympy import symbols, Xor, bool_map

    # Define symbols
    A1, A2 = symbols('A1 A2')

    # Define functions
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))

    # Attempt to find a boolean mapping between f1 and f2, and vice versa
    mapping_f2_f1 = bool_map(f2, f1)
    mapping_f1_f2 = bool_map(f1, f2)

    # Check for incorrect mappings, as XOR and XNOR should not be equivalent
    assert mapping_f2_f1 is None, "f2 should not map to f1 as equivalent"
    assert mapping_f1_f2 is None, "f1 should not map to f2 as equivalent"

    print("No issue found.")

except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
