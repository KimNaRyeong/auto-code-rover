import sympy as sp
from sympy.abc import x
import unittest
from io import StringIO
from contextlib import redirect_stdout

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    with StringIO() as f:
        print("Traceback (most recent call last):", file=f)
        for frame in tb:
            line_number = frame.lineno
            code_context = frame.line.strip() if frame.line else "Unknown"
            print(f'  File "{frame.filename}"', file=f)
            print(f"    {line_number}: {code_context}", file=f)
        print(f"{e.__class__.__name__}: {e}", file=f)
        f.seek(0)
        print(f.read())

def test_issue():
    try:
        result1 = sp.Poly(x)*x
        result2 = x*sp.Poly(x)
        result3 = -2*sp.Poly(x)
        result4 = sp.S(-2)*sp.Poly(x)
        result5 = sp.Poly(x)*sp.S(-2)

        if result1 != 'Poly(x**2, x, domain="ZZ")':
            raise AssertionError("Expected Poly(x**2, x, domain='ZZ')")
        if str(result2) != "x*Poly(x, x, domain='ZZ')":
            raise AssertionError("Expected x*Poly(x, x, domain='ZZ')")
        if str(result3) != "Poly(-2*x, x, domain='ZZ')":
            raise AssertionError("Expected Poly(-2*x, x, domain='ZZ')")
        if str(result4) != "-2*Poly(x, x, domain='ZZ')":
            raise AssertionError("Expected -2*Poly(x, x, domain='ZZ')")
        if str(result5) != "Poly(-2*x, x, domain='ZZ')":
            raise AssertionError("Expected Poly(-2*x, x, domain='ZZ')")

    except Exception as e:
        with StringIO() as f, redirect_stdout(f):
            print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_issue()
