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
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    if str(a) == '-1 + sqrt(2)' and str(sp.minimal_polynomial(b)) != '_x**2 + 2*_x - 1':
        raise AssertionError("Issue not reproduced")
    elif str(a) == '-1 + sqrt(2)' and str(sp.minimal_polynomial(b)) == '_x**2 + 2*_x - 1':
        print_stacktrace(AssertionError("Issue not fixed"))
        exit(0)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
