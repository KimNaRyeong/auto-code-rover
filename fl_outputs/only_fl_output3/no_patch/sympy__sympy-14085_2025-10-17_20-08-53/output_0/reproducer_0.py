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

def test_sympify_greek_letter():
    try:
        from sympy import sympify
        # This tries to convert the unicode string "α" (alpha) into a Sympy Symbol
        result = sympify(u"α")
        # If the issue is present, sympify will raise a SympifyError. This should not occur if the issue is fixed.
        # We assert that the operation succeeded and did not raise an exception (indicating a possible fix).
        assert result, "Sympify failed to parse the Greek letter alpha."
        print("Test passed: sympify successfully parsed the Greek letter alpha.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An error occurred while testing sympify with Greek letter alpha.") from e

if __name__ == "__main__":
    test_sympify_greek_letter()
