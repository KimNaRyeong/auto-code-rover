 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy
from reproducer import print_stacktrace

def test_mathml_printing():
    # Arccoth
    expected_arccoth = '<apply><arccoth/><ci>x</ci></apply>'
    actual_arccoth = sympy.printing.mathml(sympy.acoth(sympy.symbols('x')))
    if expected_arccoth != actual_arccoth:
        e = AssertionError(f"Expected:\n{expected_arccoth}\nActual:\n{actual_arccoth}")
        print_stacktrace(e)
        raise e

    # Arccsc
    expected_arccsc = '<apply><arccsc/><ci>x</ci></apply>'
    actual_arccsc = sympy.printing.mathml(sympy.acsc(sympy.symbols('x')))
    if expected_arccsc != actual_arccsc:
        e = AssertionError(f"Expected:\n{expected_arccsc}\nActual:\n{actual_arccsc}")
        print_stacktrace(e)
        raise e

    # Arcsec
    expected_arcsec = '<apply><arcsec/><ci>x</ci></apply>'
    actual_arcsec = sympy.printing.mathml(sympy.asec(sympy.symbols('x')))
    if expected_arcsec != actual_arcsec:
        e = AssertionError(f"Expected:\n{expected_arcsec}\nActual:\n{actual_arcsec}")
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_mathml_printing()
    print("All tests passed.")
```
This script defines a function `test_mathml_printing()` that checks the MathML printing of `acoth`, `acsc`, and `asec` functions. If the printing is incorrect, an `AssertionError` is raised with a detailed error message and a stack trace. If the printing is correct, the script prints "All tests passed."

To run the script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`. If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will print "All tests passed." and exit with code 0.