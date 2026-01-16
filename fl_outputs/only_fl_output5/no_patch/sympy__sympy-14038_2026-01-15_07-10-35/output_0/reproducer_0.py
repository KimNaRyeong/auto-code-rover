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

def main():
    from sympy import product, pi, oo
    from sympy.abc import a, n
    from sympy.functions import sinc

    try:
        # Perform the product calculation
        calculated_value = product(1 - a**2 / (n*pi)**2, [n, 1, oo])
        # The expected result should be sinc(a), not 0
        expected_result = sinc(a)

        # Check if the result of the calculation is erroneously 0
        if calculated_value == 0:
            raise AssertionError("The product calculation returned 0, which is incorrect. Expected sinc(a).")

        # If the result is not 0, check if it matches the expected sinc(a) using symbolic equality
        if not (calculated_value - expected_result).simplify() == 0:
            raise AssertionError("The product calculation did not return the expected sinc(a) value.")

        print("The issue is resolved. The correct result is returned.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
