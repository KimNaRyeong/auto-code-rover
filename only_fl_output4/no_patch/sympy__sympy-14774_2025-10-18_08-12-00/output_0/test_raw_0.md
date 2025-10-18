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

def test_latex_full_inverse_trig_names():
    from sympy import symbols, latex, acsc, asec

    x = symbols('x')

    # expected behavior
    expected_acsc_latex = '\\operatorname{arccsc}{\\left (x \\right )}'
    expected_asec_latex = '\\operatorname{arcsec}{\\left (x \\right )}'

    # actual behavior
    acsc_latex = latex(acsc(x), inv_trig_style="full")
    asec_latex = latex(asec(x), inv_trig_style="full")

    assert acsc_latex == expected_acsc_latex, f"acsc_latex ({acsc_latex}) does not match expected ({expected_acsc_latex})"
    assert asec_latex == expected_asec_latex, f"asec_latex ({asec_latex}) does not match expected ({expected_asec_latex})"

if __name__ == "__main__":
    try:
        test_latex_full_inverse_trig_names()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code
    print("No issues detected.")
    exit(0)  # Exit successfully when the issue is fixed
```