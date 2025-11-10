from sympy import Min, Poly, Symbol
import traceback
import sys

def decompogen(Min_expr, symbol):
    result = []
    while True:
        if isinstance(Min_expr, Min):
            f1 = Poly(Min_expr.arg0, symbol)
            f2 = Poly(Min_expr.arg1, symbol)
            result += [f1] + decompogen(f2, symbol)
        else:
            break
    return result

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
    x = Symbol('x')
    try:
        decompogen(Min(5,x), x)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
