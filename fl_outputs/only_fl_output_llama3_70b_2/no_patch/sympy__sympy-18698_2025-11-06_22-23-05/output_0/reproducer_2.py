import sympy as sp

def sqf_list(poly):
    factors = poly.factor()
    sqf_factors = []
    for factor in factors.args:
        multiplicity = 0
        for arg in factors.args:
            if arg == factor:
                multiplicity += 1
        sqf_factors.append((factor, multiplicity))
    return (1, sqf_factors)

def main():
    x = sp.symbols('x')
    poly = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    expected_output = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    actual_output = sqf_list(poly)
    try:
        assert actual_output == expected_output
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
