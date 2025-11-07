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

def test_diophantine_issue():
    from sympy.solvers.diophantine import diophantine
    from sympy import symbols

    n, m = symbols('n m')
    eq = n**4 + m**4 - 2**4 - 3**4

    # Test 1: m, n order
    result_1 = diophantine(eq, syms=(m, n), permute=True)
    expected_1 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}

    # Test 2: n, m order
    result_2 = diophantine(eq, syms=(n, m), permute=True)
    expected_2 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}

    assert result_1 == expected_1, f"Result 1 mismatch. Expected {expected_1}, got {result_1}"
    assert result_2 == expected_2, f"Result 2 mismatch. Expected {expected_2}, got {result_2}"

if __name__ == "__main__":
    try:
        test_diophantine_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Issue is fixed.")
    exit(0)
```