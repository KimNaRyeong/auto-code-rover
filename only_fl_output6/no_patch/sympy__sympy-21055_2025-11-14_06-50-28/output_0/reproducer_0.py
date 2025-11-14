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

def test_sympy_refine_issue():
    from sympy import symbols, Integral, sin, exp, oo, refine, Q, Abs, arg

    # Define symbols
    a, x = symbols('a x', real=True)
    # Define integral
    J = Integral(sin(x)*exp(-a*x), (x, 0, oo))
    # Evaluate integral
    evaluated_J = J.doit()
    # Use refine directly on result of J.doit()
    refined_J = refine(evaluated_J, Q.positive(a))
    
    # The refinement should have simplified the expression for a > 0
    expected_piecewise_condition = evaluated_J.args[0].cond.subs(a, Abs(a))
    try:
        # Check if condition has been correctly simplified (refined) to consider a as positive
        assert refined_J.args[0].cond != expected_piecewise_condition, "refine should have simplified the condition"
    except AssertionError as e:
        # The condition part should be different for refined_J if the refinement considered `a` as positive
        print_stacktrace(e)
        raise e
        
    # Test refine with abs and arg directly
    try:
        assert refine(abs(a), Q.positive(a)) == a, "refine should simplify abs(a) to a for a > 0"
        assert refine(arg(a), Q.positive(a)) == 0, "refine should simplify arg(a) to 0 for a > 0"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        test_sympy_refine_issue()
    except AssertionError:
        raise SystemExit(1)
    print("Issue not present or has been fixed.")
    SystemExit(0)
