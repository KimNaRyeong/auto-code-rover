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

def reproduce_issue():
    from sympy import Integral, sin, exp, var, oo, refine, Q

    var('a,x')
    J = Integral(sin(x)*exp(-a*x), (x, 0, oo))
    result = J.doit()
    refined_result = refine(J.doit(), Q.positive(a))
    refined_abs = refine(abs(a), Q.positive(a))
    refined_arg = refine(abs(a), Q.positive(a))

    # Check if refine simplifies the result correctly
    assert refined_result != result, "Refine does not simplify the expression for positive 'a'"
    # Check if refine simplifies abs(a) and arg(a) correctly
    assert refined_abs == a, "Refine does not simplify abs(a) for positive 'a'"
    assert refined_arg == 0, "Refine does not simplify arg(a) for positive 'a'"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("Issue is fixed.")
    raise SystemExit(0)
