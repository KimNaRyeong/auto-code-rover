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
    from sympy import totient
    try:
        result = totient(2.3)
        assert result == "Should not calculate totient for non-integers", "totient calculated for non-integer"
    except AssertionError as e:
        # if the assertion fails, it means the issue is present
        print_stacktrace(e)
        raise e
    except Exception as e:
        # If any other exception is raised, print its stacktrace.
        print("An unexpected error occurred:", file=sys.stderr)
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
