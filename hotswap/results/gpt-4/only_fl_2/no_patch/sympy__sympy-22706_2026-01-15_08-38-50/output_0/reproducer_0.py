# reproducer.py
from sympy import Mul, Pow, symbols

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

def reproducer():
    x = symbols('x')
    try:
        print(Mul(Pow(x, -2, evaluate=False), Pow(3, -1, evaluate=False), evaluate=False))
        print("Issue not present.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present.")

if __name__ == "__main__":
    reproducer()
