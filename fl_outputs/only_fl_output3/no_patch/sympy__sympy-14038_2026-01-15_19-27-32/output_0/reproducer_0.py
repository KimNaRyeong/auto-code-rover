# reproducer.py

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

def run_test():
    from sympy import product, oo, pi, sinc
    from sympy.abc import a, n

    expected = sinc(a)
    result = product(1 - a**2 / (n*pi)**2, [n, 1, oo])

    # Assert the issue 
    try:
        assert result != 0, "The product unexpectedly evaluates to 0."
        assert result == expected, "The result does not match the expected sinc(a) function."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Issue not present. The test passed successfully.")

if __name__ == "__main__":
    run_test()
