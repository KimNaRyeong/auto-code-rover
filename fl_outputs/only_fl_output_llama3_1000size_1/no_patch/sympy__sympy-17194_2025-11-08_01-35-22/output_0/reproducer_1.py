import sympy as sp

def reproduce_issue():
    try:
        expected = '<apply><arccoth/><ci>x</ci></apply>'
        actual = str(sp.printing.mathml(sp.acoth(sp.Symbol('x'))))
        assert actual == expected, f"Expected {expected}, got {actual}"
        
        expected = '<apply><arccsc/><ci>x</ci></apply>'
        actual = str(sp.printing.mathml(sp.acsc(sp.Symbol('x'))))
        assert actual == expected, f"Expected {expected}, got {actual}"
        
        expected = '<apply><arcsec/><ci>x</ci></apply>'
        actual = str(sp.printing.mathml(sp.asec(sp.Symbol('x'))))
        assert actual == expected, f"Expected {expected}, got {actual}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    reproduce_issue()
