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
    expected_outputs = {
        "acoth": '<apply><arccoth/><ci>x</ci></apply>',
        "acsc": '<apply><arccsc/><ci>x</ci></apply>',
        "asec": '<apply><arcsec/><ci>x</ci></apply>'
    }

    actual_outputs = {
        "acoth": sympy.printing.mathml(sympy.acoth(x)),
        "acsc": sympy.printing.mathml(sympy.acsc(x)),
        "asec": sympy.printing.mathml(sympy.asec(x))
    }

    for func, expected_output in expected_outputs.items():
        actual_output = actual_outputs[func]
        try:
            assert actual_output == expected_output, f"{func} output mismatch"
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with non-zero status code to indicate error

if __name__ == "__main__":
    check_mathml_output()
    print("No issues found.")
    exit(0)  # Exit with code 0 to indicate success
