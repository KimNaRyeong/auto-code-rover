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

def main():
    from sympy import sqrt, Rational, simplify
    try:
        # Representing the issue
        result = sqrt(8)**Rational(2, 3)
        simplified_result = simplify(result)

        # Creating a direct comparison to what the user would expect
        # which is a simplification to just '2'

        # Checking against the simplified result directly might not reflect the case accurately
        # since the `simplify` method could resolve it outside the Sympy's automatic simplification.
        # Hence we directly check if the result is not simplified initially as expected.
        assert str(result) == "2", f"Result did not simplify directly to '2', got '{result}'"
    except AssertionError as e:
        # If the AssertionError is caught, it means the issue is present.
        raise e
    except Exception as e:
        # For any other exceptions, print the stack trace.
        print_stacktrace(e)

if __name__ == "__main__":
    main()
