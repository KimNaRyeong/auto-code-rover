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

def test_parse_mathematica_greek_characters():
    from sympy.parsing.mathematica import parse_mathematica
    try:
        result = parse_mathematica('λ')
        # Assuming that, when fixed, the function should return a valid symbol/object
        # without raising exceptions.
        assert result is not None, "Failed to parse Greek character"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Exception occurred while trying to parse Greek characters with parse_mathematica") from e

if __name__ == "__main__":
    test_parse_mathematica_greek_characters()
