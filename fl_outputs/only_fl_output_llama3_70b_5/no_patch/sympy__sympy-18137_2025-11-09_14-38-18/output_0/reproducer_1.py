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
    from sympy.sets import Range, FiniteSet
    n = sp.symbols('n', integer=True)
    try:
        Range(1).intersect(FiniteSet(n))
    except TypeError as e:
        print_stacktrace(e)
        assert False, "TypeError: cannot determine truth value of Relational"

if __name__ == "__main__":
    main()
