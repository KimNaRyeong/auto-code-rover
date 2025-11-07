# Save this script as reproducer.py in the project's root directory.
# Ensure to run this in an environment where NumPy is not installed or is inaccessible to genuinely reproduce the reported issue.

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

def test_issue_sympy():
    from sympy import symbols, Sum, oo, factorial, pi
    # Attempting to reproduce a failure similar to one mentioned.
    n = symbols('n')
    expr = Sum((2**-10 * factorial(4*n) * (1103 + 26390*n) / factorial(n)**4 / 396**(4*n)), (n, 0, oo))
    pi_str = str(expr.evalf(100))
    assert pi_str.startswith('3.141'), "Pi computation failed or accuracy is compromised"
    
try:
    test_issue_sympy()
except AssertionError as e:
    print_stacktrace(e)
    raise
else:
    print("Test passed. The issue appears to be fixed.")
