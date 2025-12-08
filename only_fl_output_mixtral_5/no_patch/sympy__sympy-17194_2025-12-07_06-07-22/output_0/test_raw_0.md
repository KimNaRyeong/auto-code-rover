 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy
from reproducer import print_stacktrace

def test_mathml_printing():
    # Arccoth
    expected_arccoth = '<apply><arccoth/><ci>x</ci></apply>'
    actual_arccoth = sympy.printing.mathml(sympy.acoth(sympy.symbols('x')))
    if expected_arccoth != actual_arccoth:
        e = AssertionError(f"Expected {expected_arccoth} but got {actual_arccoth}")
        print_stacktrace(e)
        raise e

    # Arccsc
    expected_arccsc = '<apply><arccsc/><ci>x</ci></apply>'
    actual_arccsc = sympy.printing.mathml(sympy.acsc(sympy.symbols('x')))
    if expected_arccsc != actual_arccsc:
        e = AssertionError(f"Expected {expected_arccsc} but got {actual_arccsc}")
        print_stacktrace(e)
        raise e

    # Arcsec
    expected_arcsec = '<apply><arcsec/><ci>x</ci></apply>'
    actual_arcsec = sympy.printing.mathml(sympy.asec(sympy.symbols('x')))
    if expected_arcsec != actual_arcsec:
        e = AssertionError(f"Expected {expected_arcsec} but got {actual_arcsec}")
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_mathml_printing()
    print("All tests passed.")
```
The script defines a function `test_mathml_printing()` that checks the MathML printing of `acoth`, `acsc`, and `asec` functions. If the printing is incorrect, the function raises an `AssertionError` with a stack trace.

The script then calls the function and exits with code 0 if all tests pass, or raises an exception with a stack trace if any test fails.