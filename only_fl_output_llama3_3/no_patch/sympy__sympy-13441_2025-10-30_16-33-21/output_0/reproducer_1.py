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

def reproduce_issue():
    assert False, "This assertion should fail"

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 when the issue is present
    else:
        print("Issue fixed. Exiting with code 0.")
        exit(0)  # Exit with code 0 when the issue is fixed
