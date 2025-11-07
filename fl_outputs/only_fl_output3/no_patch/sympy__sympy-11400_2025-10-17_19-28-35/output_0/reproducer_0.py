# reproducer.py
from sympy import symbols, sinc, ccode, Piecewise, Ne, sin

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
    x = symbols('x')
    expected_code = '((Ne(x, 0)) ? (\n   sin(x)/x\n)\n: (\n   1\n))'
    sinc_code = ccode(sinc(x))
    piecewise_code = ccode(Piecewise((sin(x)/x, Ne(x, 0)), (1, True)))

    try:
        # Check if the output of sinc(x) is incorrect
        assert sinc_code != "// Not supported in C:\n// sinc\nsinc(x)", "sinc(x) C code generation failed"
        # Check if the output matches the expected piecewise representation
        assert piecewise_code == expected_code, "Piecewise representation does not match"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to indicate failure
    else:
        print("Issue is fixed.")
        sys.exit(0)  # Exit with code 0 to indicate success

if __name__ == "__main__":
    main()
