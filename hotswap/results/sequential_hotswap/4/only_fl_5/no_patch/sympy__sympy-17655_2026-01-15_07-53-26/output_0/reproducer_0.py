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

def test_multiplication_order_issue():
    from sympy import geometry as ge
    import sympy

    point1 = ge.Point(0, 0)
    point2 = ge.Point(1, 1)

    try:
        # This line works as expected.
        result1 = point1 + point2 * sympy.sympify(2.0)

        # This line is supposed to work similarly but raises an exception.
        result2 = point1 + sympy.sympify(2.0) * point2

        # Verifying results
        assert result1 == result2, "The results are not equal."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The expected behavior is that both lines give the same result.")

if __name__ == "__main__":
    test_multiplication_order_issue()
