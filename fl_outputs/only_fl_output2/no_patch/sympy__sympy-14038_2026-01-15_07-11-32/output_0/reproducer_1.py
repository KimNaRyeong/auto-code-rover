# reproducer.py
def main():
    try:
        from sympy import product, pi, sinc, oo
        from sympy.abc import a, n

        # Evaluating the product
        result = product(1 - a**2 / (n*pi)**2, [n, 1, oo])

        # Check if the evaluated product equals 0, which is the issue
        if result == 0:
            raise AssertionError("Product incorrectly evaluates to 0.")

        expected = sinc(a)
        assert result.equals(expected), "The result does not match sinc(a)."

        # If there is no AssertionError, print this message.
        print("The issue seems to be fixed. Exiting with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to signal error due to the assertion failing.
    except Exception as e:
        print("An unexpected error occurred:")
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
