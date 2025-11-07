# reproducer.py
from sympy import symbols, acsc, asec, latex

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

def test_latex_full_inv_trig():
    x = symbols('x')
    # Correct LaTeX representations for reference
    correct_acsc_latex = '\\operatorname{arccsc}{\\left (x \\right )}'
    correct_asec_latex = '\\operatorname{arcsec}{\\left (x \\right )}'

    try:
        # Testing `acsc` LaTeX representation
        acsc_latex = latex(acsc(x), inv_trig_style="full")
        assert acsc_latex == correct_acsc_latex, f"`acsc` LaTeX output was incorrect: {acsc_latex}"

        # Testing `asec` LaTeX representation
        asec_latex = latex(asec(x), inv_trig_style="full")
        assert asec_latex == correct_asec_latex, f"`asec` LaTeX output was incorrect: {asec_latex}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(-1)
    
    print("Issue not present, both `acsc` and `asec` are correctly represented.")
    return 0

if __name__ == "__main__":
    test_latex_full_inv_trig()
