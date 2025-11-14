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

def main():
    try:
        idiff(sp.Eq(sp.exp(sp.sympify('y'))*sp.sympify('y'), sp.sympify('x')*sp.exp(sp.sympify('x'))), sp.sympify('y'), sp.sympify('x'))
        idiff(sp.sympify('f(x)*exp(f(x)) - x*exp(x)'), sp.sympify('f(x)'), sp.sympify('x'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
