import sympy
from sympy import acoth, acsc, asec

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

def test_mathml_printing():
    x = sympy.symbols('x')

    try:
        assert sympy.printing.mathml(acoth(x)) == '<apply><arccoth/><ci>x</ci></apply>'
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    try:
        assert sympy.printing.mathml(acsc(x)) == '<apply><arccsc/><ci>x</ci></apply>'
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    try:
        assert sympy.printing.mathml(asec(x)) == '<apply><arcsec/><ci>x</ci></apply>'
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_mathml_printing()
