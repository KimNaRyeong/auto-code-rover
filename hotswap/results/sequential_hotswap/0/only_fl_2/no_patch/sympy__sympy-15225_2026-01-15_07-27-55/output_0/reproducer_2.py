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
    
    # Define XOR and its negation (XNOR)
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))

    # Run bool_map to attempt to map XNOR to XOR and vice versa
    map_result_f2_to_f1 = bool_map(f2, f1)
    map_result_f1_to_f2 = bool_map(f1, f2)

    # The expected results if mapping was performed correctly,
    # but since these are XOR and XNOR, direct mapping shouldn't be this straightforward.
    # The assertion error will be raised if the investigation doesn't reveal the issue
    # or if the bool_map incorrectly identifies the mapping between f1 and f2 as valid.
    if (map_result_f2_to_f1[0] != f1) or (map_result_f1_to_f2[0] != f2):
        raise AssertionError("bool_map did not map XOR and XNOR correctly.")

except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exiting with error status when issue is detected to signal the presence of the issue.
except Exception as e:
    print("An unexpected error occurred:", str(e))
    exit(1)
else:
    print("No issue detected, bool_map is functioning as expected.")
    exit(0)  # Exiting with success status when no issue is detected.
