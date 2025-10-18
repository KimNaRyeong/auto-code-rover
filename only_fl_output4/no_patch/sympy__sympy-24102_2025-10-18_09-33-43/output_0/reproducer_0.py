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
    try:
        from sympy.parsing.mathematica import parse_mathematica
        # Attempt to parse a Greek symbol
        result = parse_mathematica('λ')
        # If no exception is thrown, the issue is presumed to be fixed
        print("Successfully parsed: ", result)
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # If an error occurs, raise an AssertionError to indicate the issue is still present
        raise AssertionError("The parser failed to handle Greek characters.")

if __name__ == "__main__":
    main()
