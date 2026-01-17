```python
# reproducer.py

import sympy
from sympy.abc import x

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

def check_mathml_output():
    acot_mml = sympy.printing.mathml(sympy.acoth(x))
    assert acot_mml == '<apply><arccoth/><ci>x</ci></apply>', \
        f"acoth(x) MathML output incorrect. Expected '<apply><arccoth/><ci>x</ci></apply>', got {acot_mml}"

    acsc_mml = sympy.printing.mathml(sympy.acsc(x))
    assert acsc_mml == '<apply><arccsc/><ci>x</ci></apply>', \
        f"acsc(x) MathML output incorrect. Expected '<apply><arccsc/><ci>x</ci></apply>', got {acsc_mml}"

    asec_mml = sympy.printing.mathml(sympy.asec(x))
    assert asec_mml == '<apply><arcsec/><ci>x</ci></apply>', \
        f"asec(x) MathML output incorrect. Expected '<apply><arcsec/><ci>x</ci></apply>', got {asec_mml}"

if __name__ == "__main__":
    try:
        check_mathml_output()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issues found.")
    exit(0)
```