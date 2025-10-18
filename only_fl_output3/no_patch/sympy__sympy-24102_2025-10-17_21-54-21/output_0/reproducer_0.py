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

def test_parse_greek_character():
    from sympy.parsing.mathematica import parse_mathematica

    try:
        output = parse_mathematica('λ')
        # If the function returns without raising an Exception, we assume it's fixed.
        print("Issue seems to be fixed.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Raising an AssertionError to indicate issue presence.
        raise AssertionError("Failed to parse Greek characters using parse_mathematica.")

if __name__ == "__main__":
    test_parse_greek_character()
