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

def test_bell_limit():
    from sympy import Symbol, bell, oo
    n = Symbol('n')
    result = bell(n).limit(n, oo)
    expected = oo  # Expected result is infinity
    assert result == expected, "Limit of bell(n) as n->oo should be oo, found {}".format(result)

if __name__ == "__main__":
    try:
        test_bell_limit()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("Test passed. The issue is fixed.")
        raise SystemExit(0)
