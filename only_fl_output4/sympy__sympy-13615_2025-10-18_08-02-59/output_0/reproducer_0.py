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
    from sympy import Symbol, FiniteSet, Interval, Complement

    x, y = Symbol('x'), Symbol('y')  # Define symbols
    a = FiniteSet(x, y, 2)
    b = Interval(-10, 10)
    result = Complement(a, b)

    # Here we check if the issue is present. Since the expected result is not purely {x, y}
    # but rather {x, y} \ [-10,10], we assert for incorrect behavior.
    try:
        assert str(result) == "{x, y} \\ [-10, 10]", "Issue detected: Complement does not work as expected with mixture of Symbols and numbers."

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
