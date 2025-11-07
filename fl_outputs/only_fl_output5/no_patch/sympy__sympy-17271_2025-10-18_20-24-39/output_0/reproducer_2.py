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

def test_frac_with_zoo():
    from sympy import frac, zoo
    try:
        result = frac(zoo)  # This is expected to either fail or not, depending on the issue presence
        # Assume the issue is fixed if the above line does not raise an exception
        print("The issue with frac(zoo) seems to be fixed:", result)
        return True
    except TypeError as e:
        # If a TypeError is specifically caught, print the stacktrace
        print_stacktrace(e)
        return False
    except Exception as e:
        # Catching any other exceptions to ensure they don't go unnoticed
        print("An unexpected exception occurred:", e)
        print_stacktrace(e)
        return False

def main():
    issue_fixed = test_frac_with_zoo()
    if issue_fixed:
        print("Issue fixed. Exiting with code 0.")
        exit(0)
    else:
        # Raise an AssertionError if the issue is still present
        # This is to explicitly flag that the issue reproduction was successful, but the problem remains.
        raise AssertionError("The issue with frac(zoo) is still present.")

if __name__ == "__main__":
    main()
