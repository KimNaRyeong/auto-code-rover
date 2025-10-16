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

def test_inaccurate_rendering():
    from sympy import pi, E, latex, pretty

    # Evaluate the expression
    expr = pi**(1/E)

    # Expected and actual outputs for comparison
    expected_pretty = "\pi^{e^{-1}}"
    expected_str = "pi**exp(-1)"
    actual_pretty = pretty(expr)
    actual_str = str(expr)

    # Check for the presence of the issue
    if actual_pretty == expected_pretty and actual_str == expected_str:
        print("Issue fixed!")
        return True
    else:
        try:
            # Raise an AssertionError if the output is not as expected
            assert actual_pretty == expected_pretty and actual_str == expected_str, "Inaccurate rendering detected!"
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    try:
        test_inaccurate_rendering()
    except AssertionError:
        exit(1)  # Exit with error code if the issue is present
    exit(0)  # Exit with success code if the issue is fixed
