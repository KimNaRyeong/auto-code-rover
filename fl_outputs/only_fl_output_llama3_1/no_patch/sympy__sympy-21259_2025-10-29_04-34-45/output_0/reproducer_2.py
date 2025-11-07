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
    x = sp.symbols('x')
    try:
        range_obj = sp.Range(3,11,2).as_relational(x)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue is fixed")
        sys.exit(0)

if __name__ == "__main__":
    main()
