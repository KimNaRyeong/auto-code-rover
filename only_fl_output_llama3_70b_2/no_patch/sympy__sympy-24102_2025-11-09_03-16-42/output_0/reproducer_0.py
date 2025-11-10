import sys
from sympy.parsing.mathematica import mathematica, parse_mathematica

def test_mathematica():
    try:
        result = mathematica('λ')
        assert result == 'λ'
        print("mathematica function works as expected")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def test_parse_mathematica():
    try:
        result = parse_mathematica('λ')
        assert False, "parse_mathematica should raise an error"
    except SyntaxError:
        print("parse_mathematica raises a SyntaxError as expected")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

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

if __name__ == "__main__":
    test_mathematica()
    test_parse_mathematica()
