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

def check_inconsistency(expr, latex_representation, pprint_representation, assumptions={}):
    # Set assumptions for variables if provided
    for var, assumption in assumptions.items():
        sp.var(var, **assumption)
    
    # Generate LaTeX and pretty print (pprint) formats
    latex_output = sp.latex(expr)
    pprint_output = sp.pretty(expr)

    # Check consistency
    if latex_output != latex_representation or pprint_output.strip() != pprint_representation:
        raise AssertionError("Inconsistent outputs detected")

def main():
    try:
        # First Case
        x = sp.symbols('x', positive=True)
        check_inconsistency(sp.exp(-x) * sp.log(x),
                            '\\frac{1}{e^{x}} \\log{\\left (x \\right )}',
                            " -x\nℯ  ⋅log(x)",
                            assumptions={'x': {'positive': True}})
        
        # Second Case without assumptions affecting printing
        x, y = sp.symbols('x y')
        check_inconsistency(1/(x + y)/2,
                            '\\frac{1}{2 x + 2 y}',
                            "    1\n─────────\n2⋅(x + y)")
    
    except AssertionError as e:
        print_stacktrace(e)
        raise   # Re-raise the exception to ensure the script exits as non-zero when issue exists

if __name__ == '__main__':
    main()
