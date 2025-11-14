import sympy
from sympy.parsing.mathematica import mathematica, parse_mathematica

def test_parse_mathematica():
    try:
        result = parse_mathematica('λ')
        assert result == 'λ', "parse_mathematica failed to parse Greek character"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("parse_mathematica failed to parse Greek character")

def test_old_mathematica_parser():
    result = mathematica('λ')
    assert result == 'λ', "old mathematica parser failed to parse Greek character"

def main():
    try:
        test_parse_mathematica()
        print("parse_mathematica parses Greek characters successfully")
    except AssertionError as e:
        raise
    finally:
        test_old_mathematica_parser()

if __name__ == "__main__":
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

    main()
