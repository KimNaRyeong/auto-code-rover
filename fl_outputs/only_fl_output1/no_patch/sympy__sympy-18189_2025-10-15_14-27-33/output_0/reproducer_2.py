import sys

def print_stacktrace(e: Exception):
    import traceback
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

    # Define symbols
    m, n = symbols('m n')

    # Solving diophantine equation with one order of symbols
    result1 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m, n), permute=True)

    # Solving diophantine equation with another order of symbols
    result2 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n, m), permute=True)

    try:
        # Check if result changes with order of symbols despite permute=True
        assert result1 == result2, "Inconsistent results based on symbols order with permute=True"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit code 1 indicates failure

    print("Issue not present or fixed.", file=sys.stderr)
    sys.exit(0)  # Exit code 0 indicates success

if __name__ == "__main__":
    main()
