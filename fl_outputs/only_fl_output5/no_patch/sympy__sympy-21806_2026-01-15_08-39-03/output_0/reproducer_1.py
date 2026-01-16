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

def main():
    try:
        # Create a Quaternion with symbolic components
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        # Attempt to evaluate to numeric (floating point) form
        q_eval = q.evalf()
        
        # Since the original issue mentions absence of correct evalf behavior, we verify its output type
        # Checking if evalf method returns the expected numeric types for Quaternion components
        # If the components are not properly evaluated to floats, we raise an AssertionError
        for component in [q_eval.a, q_eval.b, q_eval.c, q_eval.d]:
            if not isinstance(component, sp.Float):
                raise AssertionError("Quaternion evalf method does not properly evaluate to float.")
        
    except AssertionError as e:
        # If AssertionError is caught, it implies the issue is still present
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        # For any unexpected exception, print the stack trace and exit with an error code.
        print_stacktrace(e)
        exit(1)
    else:
        # No exceptions were raised, issue is assumed to be fixed, or evalf method behaves as expected
        print("No issue detected.")
        exit(0)

if __name__ == "__main__":
    main()
