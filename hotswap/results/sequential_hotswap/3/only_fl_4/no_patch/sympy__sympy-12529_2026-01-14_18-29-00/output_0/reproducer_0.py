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
        # Assuming that if no error is raised, it's still an issue
        # because totient should not accept non-integer values
        assert isinstance(result, Exception), "Expected an error for non-integer argument"
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exiting with a non-zero code since the issue is still present
    
    print("Test passed: Totient function correctly raises an error for non-integer input.")
    exit(0)

if __name__ == "__main__":
    main()
