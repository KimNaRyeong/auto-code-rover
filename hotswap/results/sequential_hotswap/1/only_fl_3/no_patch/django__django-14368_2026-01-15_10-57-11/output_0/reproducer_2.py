# reproducer.py
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

def test_parse_datetime_with_space():
    from django.utils.dateparse import parse_datetime
    test_datetime_string = '2012-04-23T10:20:30.400 -02'
    parsed_datetime = parse_datetime(test_datetime_string)
    try:
        assert parsed_datetime is not None, "Failed to parse ISO-8601 datetime string with space before timezone."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_parse_datetime_with_space()
        print("Test passed: Issue seems to be resolved")
        sys.exit(0)  # 0 indicates the issue described is not present
    except AssertionError:
        sys.exit(1)  # Non-zero exit code indicates the script caught the issue
