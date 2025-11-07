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

def test_sqf_consistency():
    from sympy import symbols, sqf_list

    x = symbols('x')
    # Test case 1
    expr1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    expected1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    result1 = sqf_list(expr1)
    assert result1 == expected1, f"Expected {expected1}, got {result1}"

    # Test case 2
    expr2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    expected2 = (1, [(x - 2, 1), (x**2 - 1, 2)])
    result2 = sqf_list(expr2)
    assert result2 == expected2, f"Expected {expected2}, got {result2}"

if __name__ == "__main__":
    try:
        test_sqf_consistency()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
