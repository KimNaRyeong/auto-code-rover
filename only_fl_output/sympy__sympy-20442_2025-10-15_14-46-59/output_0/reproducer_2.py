from sympy.physics.units import convert_to, joules, s
from sympy import symbols

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

def test_convert_to_issue():
    # Correcting the units to use `joules` and conversion format
    J = joules
    try:
        # Attempt conversion as stated in the issue
        result = convert_to(J * s, J)
        # We check specifically for the reported incorrect behavior
        expected_behavior = J * s
        if result != expected_behavior:
            raise AssertionError(f"Expected {expected_behavior}, got {result}")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with the error code to indicate failure
    
    # If the script reaches this point, it means the issue is not present or has been fixed
    print("Issue not present or has been fixed.")
    sys.exit(0)

if __name__ == "__main__":
    test_convert_to_issue()
