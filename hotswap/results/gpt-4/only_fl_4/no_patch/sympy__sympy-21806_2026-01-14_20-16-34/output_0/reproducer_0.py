# reproducer.py

import sympy as sp


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


def test_quaternion_evalf():
    try:
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        evaluated_q = q.evalf()  # Attempt to evaluate the quaternion
        
        # Check if 'evalf' method properly evaluated the quaternion to numeric values
        for component in evaluated_q.args:
            if not component.is_Number:
                raise AssertionError("Quaternion.evalf() does not properly evaluate to numeric values.")
        
        # If it reaches here, it means values are numeric and there's no issue
        print("Quaternion 'evalf' method works as expected.")
    except Exception as e:
        print_stacktrace(e)
        raise


if __name__ == "__main__":
    try:
        test_quaternion_evalf()
    except AssertionError:
        # If an AssertionError is caught, it indicates that the issue is still present.
        print("The issue with Quaternion's evalf method being unoverridden or malfunctioning is still present.")
        exit(1)  # Exit with code 1 to indicate the issue is present.
    except Exception as error:
        # For any other kind of exception, print the exception and exit with code 1.
        print(f"An unexpected error occurred: {error}")
        exit(1)
    else:
        # If no exceptions are caught, assume issue is fixed and exit with code 0.
        exit(0)
