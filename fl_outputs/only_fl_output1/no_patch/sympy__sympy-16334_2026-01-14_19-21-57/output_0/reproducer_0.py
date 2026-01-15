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
    from sympy import symbols
    from sympy.abc import x, y, z
    p = symbols('p', real=True, zero=False)
    q = symbols('q', zero=True)

    # The issue is that (q**p).is_positive does not correctly return False
    assert (q**p).is_positive is False, f"Expected (q**p).is_positive to be False, got {(q**p).is_positive}"

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)  # Non-zero exit code to indicate failure
    print("Test passed")
    raise SystemExit(0)  # Zero exit code to indicate success
