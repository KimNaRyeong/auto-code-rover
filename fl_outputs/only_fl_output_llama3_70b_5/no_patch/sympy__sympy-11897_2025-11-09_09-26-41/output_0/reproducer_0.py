import sympy as sp

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
    x = sp.var('x', positive=True)
    expr1 = sp.exp(-x) * sp.log(x)
    latex_output1 = sp.latex(expr1)
    pretty_output1 = sp.pprint(expr1)
    assert latex_output1.replace('\\', '') == str(pretty_output1).replace('*', '⋅'), f"LaTeX output: {latex_output1}, Pretty output: {pretty_output1}"

    x, y = sp.var('x y')
    expr2 = 1 / (x + y) / 2
    latex_output2 = sp.latex(expr2)
    pretty_output2 = sp.pprint(expr2)
    assert latex_output2.replace('\\', '') == str(pretty_output2).replace('*', '⋅'), f"LaTeX output: {latex_output2}, Pretty output: {pretty_output2}"

try:
    test_latex_pretty_printer_consistency()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
