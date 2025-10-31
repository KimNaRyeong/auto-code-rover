import sympy as sp
from sympy import symbols, oo
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        n = symbols('n')
        result = sp.bell(n).limit(n, oo)
        assert result == oo
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
