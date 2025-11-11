import sympy as sp

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

def idiff(eq, y, x):
    try:
        if not isinstance(eq, sp.Eq):
            raise ValueError("expecting Eq but got: %s" % type(eq))
        if not (isinstance(y, str) and isinstance(x, str)):
            raise ValueError("expecting string symbol(s) but got: %s" % y)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

def main():
    try:
        idiff(sp.sympify('y*exp(y)-x*exp(x)'), 'y', 'x')
        idiff(sp.sympify('f(x)*exp(f(x)) - x*exp(x)'), 'f(x)', 'x')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
