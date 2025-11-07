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
    from sympy import Max, Symbol, Piecewise

    a, b = Symbol('a'), Symbol('b')
    try:
        result = Max(a, b).rewrite(Piecewise)
        expected = Piecewise((a, a>b), (b, True))
        # We'll use str comparison, direct SymPy comparison may be more involved due to symbolic nature
        assert str(result) == str(expected), f"Expected {expected}, got {result}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    except Exception as e:
        print_stacktrace(e)
        raise e
    else:
        print("Issue not present.")
        
if __name__ == "__main__":
    main()
