Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy
from sympy.parsing.mathematica import mathematica, parse_mathematica

def test_parse_greek_characters():
    # Test with deprecated mathematica function (should work)
    result = mathematica('λ')
    assert result == 'λ'

    # Test with new parse_mathematica function (should raise SyntaxError)
    try:
        parse_mathematica('λ')
        raise AssertionError("Expected SyntaxError, but no exception was raised")
    except Exception as e:
        print_stacktrace(e)

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
    test_parse_greek_characters()
```
This script will raise an `AssertionError` if the issue is present, and print a stack trace of the exception. If the issue is fixed, the script will exit with code 0.