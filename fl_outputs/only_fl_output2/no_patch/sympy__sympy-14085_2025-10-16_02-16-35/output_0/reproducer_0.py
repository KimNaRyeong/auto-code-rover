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

def reproduce_sympify_issue():
    from sympy import sympify, Symbol, SympifyError

    try:
        # Attempt to sympify a unicode Greek character
        result = sympify(u"α")
        # Assert that the result is an instance of Symbol for it to be considered fixed
        assert isinstance(result, Symbol), "Result is not an instance of Symbol"
    except SympifyError as e:
        print_stacktrace(e)
        raise AssertionError("sympify(u'α') does not work") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected error occurred") from e

if __name__ == "__main__":
    reproduce_sympify_issue()
