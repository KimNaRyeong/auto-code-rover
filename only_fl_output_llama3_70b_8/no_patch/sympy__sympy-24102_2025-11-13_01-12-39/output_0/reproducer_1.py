import sympy
from sympy.parsing.mathematica import mathematica, parse_mathematica

def test_parse_mathematica():
    try:
        result = parse_mathematica('λ')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Cannot parse Greek characters in parse_mathematica")

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

if __name__ == "__main__":
    test_parse_mathematica()
