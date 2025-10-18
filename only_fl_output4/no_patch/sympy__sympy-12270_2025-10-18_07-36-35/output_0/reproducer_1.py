from sympy import Symbol, I, Mul

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

def test_extract_multiplicatively():
    x, y = Symbol('x'), Symbol('y')

    # Focus on the cases expected to demonstrate the issue
    buggy_cases = [
        # The issue was previously misunderstood; let's check the actual behavior.
        # The expected behavior is now checked after a correct understanding of the problem.
        ((-2 - 4*I).extract_multiplicatively(-2), 1 + 2*I),
        ((-2*x - 4*y - 8).extract_multiplicatively(-2), Mul(-1, x + 2*y + 4, evaluate=False)),
    ]

    for input_value, expected in buggy_cases:
        result = input_value
        try:
            assert result == expected, f"expected {expected} but got {result}"
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
        print("Test passed.")
    except AssertionError:
        exit(1)
