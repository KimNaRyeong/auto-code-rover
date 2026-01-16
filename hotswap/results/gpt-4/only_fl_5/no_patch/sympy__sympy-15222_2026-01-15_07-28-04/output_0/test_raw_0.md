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

def test_subs_hashing_problem():
    from sympy import symbols, Subs

    x, y, a, z = symbols('x y a z')
    subs1 = Subs(x+y, (a,), (4,))
    subs2 = Subs(x+y, (a,), (a,))
    subs2_modified = subs2.subs(a, z)
    # Expect this to be `Subs(x + y, (a,), (z,))`
    expected_subs = Subs(x+y, (a,), (z,))

    try:
        assert subs2_modified == expected_subs, "Subs hashing problem detected"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("No issues detected.")

if __name__ == "__main__":
    try:
        test_subs_hashing_problem()
    except AssertionError:
        exit(1)  # Exit with non-zero if there's an issue detected
    exit(0)
```