import sympy as sp

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

def test_degree_of_rational_function():
    x = sp.symbols('x')
    # Attempt to compute the degree of the rational function (x-2)/(x**2+1)
    try:
        degree_result = sp.degree((x-2)/(x**2+1), x)
        assert degree_result != 1, "Degree should not be computed as 1 for a rational function."
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        # Catch unexpected errors and print their stacktrace
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_degree_of_rational_function()
    except AssertionError:
        # An AssertionError indicates the issue is present
        exit(1)
    except Exception:
        # Any other exception should not crash the program
        exit(1)
    # If no exception is caught, the issue is not present
    exit(0)
