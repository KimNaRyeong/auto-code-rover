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

def reproduce_issue():
    from sympy import symbols, acsc, asec, latex, Function
    x = symbols('x')
    
    # Incorrect function names workaround
    class acsc_fixed(Function):
        @classmethod
        def eval(cls, arg):
            return acsc(arg)
    
    class asec_fixed(Function):
        @classmethod
        def eval(cls, arg):
            return asec(arg)
    
    # Test for full inverse trig function names
    try:
        latex_acsc_full = latex(acsc_fixed(x), inv_trig_style="full")
        expected_acsc = '\\arccsc{\\left (x \\right )}'
        latex_asec_full = latex(asec_fixed(x), inv_trig_style="full")
        expected_asec = '\\arcsec{\\left (x \\right )}'

        assert latex_acsc_full == expected_acsc, f"Expected {expected_acsc}, got {latex_acsc_full}"
        assert latex_asec_full == expected_asec, f"Expected {expected_asec}, got {latex_asec_full}"
        print("Issue fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    reproduce_issue()
