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

def test_simplify_pulls_constant_from_integral():
    from sympy import symbols, Integral, simplify

    x, y, z, n = symbols('x y z n')
    original_expr = Integral(x*y - z, x)
    simplified_expr = simplify(original_expr)

    expected_expr = y * Integral(x, x) - z * Integral(1, x)

    assert simplified_expr == expected_expr, "Simplify did not pull out the constant term correctly"

if __name__ == "__main__":
    try:
        test_simplify_pulls_constant_from_integral()
        print("Test passed. The issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
```