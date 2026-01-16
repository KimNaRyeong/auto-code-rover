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
    try:
        import sympy as sm

        t, t0, tf = sm.symbols('t t0 tf')
        x = sm.Function('x')(t)
        y = sm.Function('y')(t)
        J = sm.Integral((x - y)**2, (t, t0, tf))

        # This is where the issue is expected to be shown
        sum_result = J.as_sum(20, 'trapezoid')

        # The assertion below fails if the result is evaluated instead of 
        # being an unevaluated Sum which is the bug we are validating
        assert isinstance(sum_result, sm.Sum), "Expected an unevaluated Sum object"

    except Exception as e:
        print_stacktrace(e)
        # Exiting with nonzero code to indicate an error state due to the issue being present
        exit(1)
    else:
        # Exit with code 0 indicating the test passed/issue has been resolved
        exit(0)

if __name__ == "__main__":
    main()
