```python
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

def test_sympy_mathml():
    import sympy

    # Testing acotanh -> should be arccoth
    try:
        mathml_output = sympy.printing.mathml(sympy.acoth(sympy.Symbol('x')))
        assert mathml_output == '<apply><arccoth/><ci>x</ci></apply>', "Incorrect MathML for acotanh"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Testing arcsin -> should be arccsc
    try:
        mathml_output = sympy.printing.mathml(sympy.acsc(sympy.Symbol('x')))
        assert mathml_output == '<apply><arccsc/><ci>x</ci></apply>', "Incorrect MathML for arcsin"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Testing arcsec
    try:
        mathml_output = sympy.printing.mathml(sympy.asec(sympy.Symbol('x')))
        assert mathml_output == '<apply><arcsec/><ci>x</ci></apply>', "Incorrect MathML for arcsec"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sympy_mathml()
    except AssertionError:
        exit(1)
    else:
        exit(0)
```