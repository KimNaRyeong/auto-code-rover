```python
# reproducer.py

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


def test_latex_pretty_printer_consistency():
    from sympy import var, exp, log, latex, pprint
    import io
    import sys

    try:
        # Test 1: exp(-x)*log(x)
        var('x', positive=True)
        latex_str_1 = latex(exp(-x)*log(x))
        expected_latex_1 = '\\frac{1}{e^{x}} \\log{\\left (x \\right )}'
        assert latex_str_1 == expected_latex_1, f"LaTeX printer inconsistency: {latex_str_1} != {expected_latex_1}"

        old_stdout_1 = sys.stdout
        sys.stdout = io.StringIO()
        pprint(exp(-x)*log(x))
        pretty_str_1 = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout_1

        expected_pretty_1 = "-x\nℯ  ⋅log(x)"
        if not pretty_str_1 == expected_pretty_1:
            raise AssertionError(f"Pretty printer inconsistency: {pretty_str_1} != {expected_pretty_1}")

        # Test 2: 1/(x + y)/2
        var('x y')
        latex_str_2 = latex(1/(x + y)/2)
        expected_latex_2 = '\\frac{1}{2 x + 2 y}'
        assert latex_str_2 == expected_latex_2, f"LaTeX printer inconsistency: {latex_str_2} != {expected_latex_2}"

        old_stdout_2 = sys.stdout
        sys.stdout = io.StringIO()
        pprint(1/(x + y)/2)
        pretty_str_2 = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout_2

        expected_pretty_2 = "1\n─────────\n2⋅(x + y)"
        if not pretty_str_2 == expected_pretty_2:
            raise AssertionError(f"Pretty printer inconsistency: {pretty_str_2} != {expected_pretty_2}")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_latex_pretty_printer_consistency()

```

This script tests the consistency between LaTeX and pretty printers in two given scenarios as per the issue description. It captures the output from both printers and compares it to the expected strings. If there's an inconsistency, it raises an `AssertionError` with a detailed message about what was expected vs. what was received. The `print_stacktrace` function is used to provide detailed error information if the script fails the assertions.
