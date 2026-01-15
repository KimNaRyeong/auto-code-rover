# reproducer.py
from sympy import *
from sympy.abc import a, n

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

def main():
    try:
        # This is the expression that is mistakenly evaluated to 0
        evaluated_product = product(1 - a**2 / (n*pi)**2, [n, 1, oo])
        
        # The correct behavior is that it should not evaluate to zero,
        # instead, it should ideally be equivalent to sinc(a)
        # For the purpose of demonstration, I'm checking against zero
        # but real production code would involve a correct evaluation
        # potentially comparing simplifications or series expansions with sinc(a)
        
        assert evaluated_product != 0, "The product incorrectly evaluates to 0."
        
        print("Issue not present, evaluated expression:", evaluated_product)

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
