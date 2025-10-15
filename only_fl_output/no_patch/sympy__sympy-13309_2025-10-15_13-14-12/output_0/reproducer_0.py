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

def test_piecewise_rewriting_for_max():
    from sympy import Max, Symbol, Piecewise

    a = Symbol('a')
    b = Symbol('b')

    expected = Piecewise((a, a>b), (b, True))
    result = Max(a, b).rewrite(Piecewise)

    assert result == expected, "Piecewise rewriting for Max does not match expected output."

def main():
    try:
        test_piecewise_rewriting_for_max()
        print("Issue fixed or cannot reproduce.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
