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

def main():
    from sympy import symbols, Xor, bool_map
    from sympy.logic.boolalg import _finger
    from collections import defaultdict
    A1, A2, A3 = symbols('A1 A2 A3')
    f1 = Xor(A1, A2, A3)
    f2 = ~(Xor(A1, A2, A3))
    
    # Adjusting the logic to correctly raise an error if the issue is detected
    try:
        result = bool_map(f1, f2)
        # If finding an equivalent mapping is considered a failure (an issue), then assert the opposite
        correct_result = (None, {A1: A1, A3: A3, A2: A2}) # Assume this is what a correct output should look like
        assert result == correct_result, "bool_map incorrectly found an equivalent mapping which indicates an issue."
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # To ensure the script raises an error if an issue is detected
    
    # Checking the fingerprint routine
    try:
        a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
        b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
        # Expect different fingerprints for a and b to assert success; identical indicates a flaw.
        assert a != b, "Fingerprints are identical, which indicates an issue."
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # To ensure the script exits indicating an issue was found
    
    print("Finished executing reproducer.py without detecting any issues.")

if __name__ == "__main__":
    main()
