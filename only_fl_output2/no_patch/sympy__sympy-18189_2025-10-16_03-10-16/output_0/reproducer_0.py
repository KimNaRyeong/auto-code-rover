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
    from sympy import symbols, diophantine

    m, n = symbols('m n')
    equation = n**4 + m**4 - 2**4 - 3**4

    try:
        result1 = diophantine(equation, syms=(m, n), permute=True)
        result2 = diophantine(equation, syms=(n, m), permute=True)

        assert result1 == result2, "The results should be the same regardless of the symbols' order"

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
