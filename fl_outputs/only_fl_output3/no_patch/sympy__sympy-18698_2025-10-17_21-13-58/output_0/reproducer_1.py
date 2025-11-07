import sympy as sp

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

def test_sqf_list():
    x = sp.symbols('x')

    # Case 1
    expr1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    expected1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    
    # Case 2
    expr2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    expected2 = (1, [(x - 2, 1), (x**2 - 1, 2)])

    try:
        assert sp.sqf_list(expr1) == expected1, "Case 1 output mismatch"
        assert sp.sqf_list(expr2) == expected2, "Case 2 output mismatch"
        print("No issues detected with sqf_list outputs.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        test_sqf_list()
    except AssertionError:
        # Exit with non-zero code to indicate error
        exit(1)
    else:
        # Exit with zero to indicate success
        exit(0)
