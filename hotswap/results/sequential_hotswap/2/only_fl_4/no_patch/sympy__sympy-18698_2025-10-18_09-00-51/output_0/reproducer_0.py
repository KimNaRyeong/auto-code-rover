from sympy import symbols, sqf_list

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

def test_sqf_list_consistency():
    x = symbols('x')

    # First example (where the issue is suspected)
    expr1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    result1 = sqf_list(expr1)
    expected_result1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    assert result1 == expected_result1, "First example output is not as expected."

    # Second example (working as expected)
    expr2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    result2 = sqf_list(expr2)
    expected_result2 = (1, [(x - 2, 1), (x**2 - 1, 2)])
    assert result2 == expected_result2, "Second example output is not as expected."

if __name__ == "__main__":
    try:
        test_sqf_list_consistency()
        print("All tests passed successfully.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1) from e
