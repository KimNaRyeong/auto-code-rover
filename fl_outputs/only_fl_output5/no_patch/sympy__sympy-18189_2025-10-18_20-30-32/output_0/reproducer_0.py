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

def reproduce_issue():
    from sympy import symbols, diophantine

    m, n = symbols('m n')

    # First order of symbols
    result1 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True)

    # Second order of symbols
    result2 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True)

    # Assert both results are equal
    assert result1 == result2, "diophantine returns incomplete results depending on symbols order with permute=True"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    print("No issue detected.")
