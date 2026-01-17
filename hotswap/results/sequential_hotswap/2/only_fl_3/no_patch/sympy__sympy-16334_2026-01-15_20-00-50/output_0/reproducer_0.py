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

def test_issue():
    from sympy import symbols, ask, Q
    from sympy.abc import x, y, z
    p = symbols('p', real=True, zero=False)  # Define a symbol p that is real and not zero
    q = symbols('q', zero=True)  # Define a symbol q that is zero
    result = (q**p).is_positive  # Check if q**p is positive
    
    # Since 0**a (where a is real and non-zero) should always be 0 or `zoo`, and hence non-positive,
    # the expected result should be False.
    assert result is False, "The expression's positivity evaluation did not return False."

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
