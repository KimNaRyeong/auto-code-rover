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
    from sympy import symbols, Poly, polys
    x, y, z = symbols('x y z')

    try:
        # Attempt to create Poly with domain 'RR[y,z]'
        Poly(1.2*x*y*z, x, domain='RR[y,z]')

        # If Poly creation passes without errors, we assume the issue is fixed.
        print("Issue seems to be fixed. No AssertionError raised.")
    except polys.polyerrors.OptionError as e:
        print_stacktrace(e)
        assert False, "Expected an OptionError due to invalid domain specification"

if __name__ == "__main__":
    main()
