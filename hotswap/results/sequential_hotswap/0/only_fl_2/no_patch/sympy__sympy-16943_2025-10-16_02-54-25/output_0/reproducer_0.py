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

def test_fps_behavior():
    from sympy import Symbol, fps
    x = Symbol('x')
    try:
        # Generate a formal power series
        p = fps(x ** 2)
        # Ensure that p is an instance of FormalPowerSeries
        assert hasattr(p, "truncate"), f"Expected 'FormalPowerSeries', got '{type(p).__name__}'"

        # Attempt to access the formal power series using indexing.
        # This line should not raise a TypeError when fixed.
        _ = p[0]  # Accessing the first term of the series for verification.
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    except Exception as e:
        print_stacktrace(e)
        # The following line re-raises the last exception.
        raise AssertionError("An unexpected error occurred, indicating the issue is still present.")

if __name__ == "__main__":
    test_fps_behavior()
