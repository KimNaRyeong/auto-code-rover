def main():
    try:
        from sympy import Symbol, Mul, Pow

        a = Symbol('a')
        u = Symbol('u')

        a2inv = Pow(Mul(a, a, evaluate=False), -1, evaluate=False)
        d = Mul(-2, u, a2inv, evaluate=False)

        expected_output = "-2*u/(a*a)"
        actual_output = str(d)

        assert actual_output == expected_output, f"Output mismatch: expected {expected_output}, got {actual_output}"
        print("Issue not present. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        raise


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


if __name__ == "__main__":
    main()
