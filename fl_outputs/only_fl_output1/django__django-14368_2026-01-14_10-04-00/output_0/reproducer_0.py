# reproducer.py

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_datetime_parsing():
    from django.utils.dateparse import parse_datetime

    # This is the string that illustrates the issue
    datetime_str_with_space = "2012-04-23T10:20:30.400 -02"

    # Attempt to parse it
    result = parse_datetime(datetime_str_with_space)

    # The issue implies parse_datetime returns None for valid ISO-8601 with spaces before timezone
    if result is None:
        raise AssertionError("Failed to parse ISO-8601 datetime string with space before timezone.")

    print(f"Successfully parsed datetime: {result}")

def main():
    try:
        test_datetime_parsing()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("No issues detected.")
        raise SystemExit(0)

if __name__ == "__main__":
    main()
