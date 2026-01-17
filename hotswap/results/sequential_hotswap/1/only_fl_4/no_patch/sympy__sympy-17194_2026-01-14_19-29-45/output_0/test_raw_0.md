```python
import sympy
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
    x = sympy.symbols('x')

    expected_acoth = '<apply><arccoth/><ci>x</ci></apply>'
    result_acoth = sympy.printing.mathml(sympy.acoth(x))
    assert result_acoth == expected_acoth, f"Expected {expected_acoth}, got {result_acoth}"

    expected_acsc = '<apply><arccsc/><ci>x</ci></apply>'
    result_acsc = sympy.printing.mathml(sympy.acsc(x))
    assert result_acsc == expected_acsc, f"Expected {expected_acsc}, got {result_acsc}"

    expected_asec = '<apply><arcsec/><ci>x</ci></apply>'
    result_asec = sympy.printing.mathml(sympy.asec(x))
    assert result_asec == expected_asec, f"Expected {expected_asec}, got {result_asec}"

    print("No issues found.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)
```