import sympy as smp

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
    try:
        q, u = smp.symbols(('q:2', 'u:2'))
        if type(q) != tuple or not all(isinstance(x, smp.Function) for x in q):
            raise AssertionError("Expected tuple of Function instances but got <class 'sympy.core.symbol.Symbol'>")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
