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
        # Attempt to execute totient with a non-integer number
        result = totient(2.3)
        # If no error is raised, this is incorrect behavior as per the issue description
        raise AssertionError("The totient function incorrectly accepts non-integer input without raising an error.")

    except TypeError as expected:
        # Correct behavior: a TypeError should be raised for non-integer inputs
        print("Correct behavior detected: TypeError raised for non-integer input, indicating the issue is fixed.")
        exit(0)

    except Exception as e:
        # If any other exception is caught, print the stack trace
        print("Unexpected error encountered.")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print_stacktrace(error)
        exit(1)  # Exit with error code if AssertionError is caught directly
