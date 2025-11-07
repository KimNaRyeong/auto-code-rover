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

def test_sympy_fps():
    from sympy import Symbol, fps

    x = Symbol('x')
    try:
        p = fps(x ** 2)
        # Since fps did not return a formal power series object, an assertion error is raised
        assert p.is_Pow, "fps did not return a formal power series for a power"

        # Attempt to index, expecting it to fail if p is not a formal power series
        try:
            _ = p[0]
        except Exception as e:
            # If indexing fails due to type, it confirms the issue.
            print_stacktrace(e)
            raise AssertionError("fps returned type does not support indexing")
    except AssertionError as ae:
        print_stacktrace(ae)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error occurred")

if __name__ == "__main__":
    try:
        test_sympy_fps()
        print("SUCCESS: The issue has been fixed or could not be reproduced.")
    except AssertionError:
        exit(1)
