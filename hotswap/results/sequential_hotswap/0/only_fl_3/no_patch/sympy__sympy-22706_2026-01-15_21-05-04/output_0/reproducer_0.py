# reproducer.py
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
    from sympy import symbols, Mul, Pow
    
    x = symbols('x')
    try:
        expr = Mul(Pow(x, -2, evaluate=False), Pow(3, -1, evaluate=False), evaluate=False)
        print(expr)  # The issue is expected to occur here
        # If the script reaches this point, it means no IndexError occurred,
        # which is considered as the issue being fixed.
    except IndexError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from None
    
if __name__ == "__main__":
    main()
