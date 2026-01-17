from sympy import Poly, symbols, S

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

def test_issue():
    x, y, z = symbols("x y z")
    try:
        # Attempting to trigger the specified issue
        poly = Poly(1.2*x*y*z, x, domain='RR[y,z]')
        # If the above line runs without raising an exception, the issue is presumed to have been fixed.
        return True 
    except Exception as e:
        # If an exception is caught, it's printed and the presence of the issue is confirmed
        print_stacktrace(e)
        return False

if __name__ == "__main__":
    if not test_issue():
        raise AssertionError("The issue with specifying Poly domain as 'RR[y,z]' is still present.")
    else:
        # Exit with code 0 indicating no error/issue
        print("No issue detected with specifying Poly domain as 'RR[y,z]'.")
