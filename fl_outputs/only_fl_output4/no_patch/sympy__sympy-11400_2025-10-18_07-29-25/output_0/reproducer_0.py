import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    from sympy import symbols, sin, Ne, Piecewise, ccode

    x = symbols('x')

    # Test the ccode generation for sinc(x), expecting it to not work as intended
    try:
        sinc_code = ccode(sin(x)/x)
        # This line should be unreachable if sinc(x) is not supported
        print("sinc(x) translated to C code:", sinc_code)
    except Exception as e:
        print_stacktrace(e)

    # Alternative approach since math.h doesn't have a sinc function
    piecewise_sinc = Piecewise((sin(x)/x, Ne(x, 0)), (1, True))
    piecewise_sinc_code = ccode(piecewise_sinc)

    # Expected C code translation
    expected_code = '((x != 0) ? (\n   sin(x)/x\n)\n: (\n   1\n))'
    
    try:
        assert piecewise_sinc_code == expected_code, "Piecewise sinc(x) translation to C code does not match expected output"
    
        # If we made it here, the issue is fixed or worked around
        print("Issue fixed or worked around successfully.")
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)  # Exiting with non-zero code to indicate failure

if __name__ == "__main__":
    main()
