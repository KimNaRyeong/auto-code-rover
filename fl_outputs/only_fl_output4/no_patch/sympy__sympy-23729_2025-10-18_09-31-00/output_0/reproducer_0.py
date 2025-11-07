# reproducer.py
from sympy import symbols, pprint
from sympy.printing.julia import julia_code

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
    x, y, A = symbols('x y A')
    try:
        julia_code_str = julia_code(x**2*y*A**3)
        # Check for incorrect spacing around the operators which raises Julia syntax error
        # Expectation: (x .^ 2 .* y) * A ^ 3
        assert julia_code_str == "(x .^ 2 .* y) * A ^ 3", "Invalid Julia code generated"
    except Exception as e:
        print_stacktrace(e)
        exit(1) # Exit with a non-zero exit code to indicate failure
    # If the assertion passes, implying the issue has been fixed, then print the success message.
    print("Success: The issue has been fixed.")
    exit(0)

if __name__ == "__main__":
    main()
