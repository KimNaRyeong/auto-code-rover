# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_test():
    from sympy import degree, symbols
    x = symbols('x')
    try:
        deg = degree((x-2)/(x**2+1), x)
        # Check if the result is incorrect or SymPy does not raise an error for computing the degree of a rational function
        assert deg != 1, f"Unexpected degree result: {deg}. Expected a different result or error for a rational function."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("SymPy did not behave as expected when computing degree of a rational function.") from None

if __name__ == "__main__":
    try:
        run_test()
        print("The issue has been resolved.")
    except AssertionError as e:
        sys.exit(1)
