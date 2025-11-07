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
    from sympy import sqrt, I, cos, pi, asinh, cosh
    
    # Define variables and expressions
    a = 2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3
    b = 2*sqrt(2)*I*cosh(pi/6 + asinh(5*sqrt(2)/2)/3)/3

    # Evaluate the expressions to floating-point numbers
    a_val = a.evalf()
    b_val = b.evalf()
    
    # Use an assertion to determine if there's a significant discrepancy
    try:
        # In this case, an issue where the numeric evaluation of 'a' and 'b'
        # does not match indicates the presence of the mentioned simplification error.
        assert abs(a_val - b_val) < 1e-10, "a and b should have been numerically equivalent."
    except AssertionError as error:
        # Print a detailed stack trace upon catching an assertion error
        print_stacktrace(error)
        raise

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        # If an AssertionError was raised, exit with a non-zero code (indicating failure)
        exit(1)
    # If no error was raised, exit with code 0 (indicating success)
    exit(0)
