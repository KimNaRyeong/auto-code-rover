import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    from django.utils.dateparse import parse_time

    test_strings = [
        # This is arguably an invalid input but gets accepted
        "0:5: ",
    ]

    for ts in test_strings:
        try:
            # Attempt to parse the time
            result = parse_time(ts)
            # We specifically expect None or an error for invalid inputs, not a datetime.time object
            assert result is None, f"Unexpectedly succeeded for input '{ts}'"
        except Exception as e:
            # If any other error is caught, print the stacktrace
            print_stacktrace(e)
            sys.exit(1)
    
    # If we reach this point without errors, it means the issue is still present or
    # the behavior is as expected if the script is meant to fail for current acceptance of such inputs
    print("Test completed successfully. The issue is still present or the behavior is as expected.")
    sys.exit(0)

if __name__ == "__main__":
    main()
