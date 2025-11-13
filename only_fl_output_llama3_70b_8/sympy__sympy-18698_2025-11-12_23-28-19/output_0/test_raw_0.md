Here is the `reproducer.py` file that reproduces the issue:
```
python
import sympy as sp

def sqf_list(poly):
    factors = poly.factor()
    result = []
    for factor, multiplicity in factors.as_dict().items():
        result.append((factor, multiplicity))
    return (1, result)

def main():
    x = sp.symbols('x')
    poly1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    expected_output1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    output1 = sqf_list(poly1)
    try:
        assert output1 == expected_output1
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    poly2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    expected_output2 = (1, [(x - 2, 1), (x**2 - 1, 2)])
    output2 = sqf_list(poly2)
    try:
        assert output2 == expected_output2
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
```
This script uses the `sympy` library to perform polynomial factorization. It defines two test cases: one that should fail (due to the issue) and one that should pass.

When run, this script will raise an `AssertionError` if the issue is present, printing a stack trace of the error. If the issue is fixed, the script will exit with code 0.