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

def test_parse_time():
    from django.utils.dateparse import parse_time
    # Providing a known 'invalid' time format based on the description.
    # This time technically shouldn't be valid, per the stricter requirements being requested.
    time_string = '0:5: '
    try:
        result = parse_time(time_string)
        # It's considered an issue, if the parse_time does not raise an error for this input.
        assert result is None, f"Unexpected parsing success for input '{time_string}'"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_parse_time()
    except AssertionError:
        sys.exit(1)
    print("Issue reproduction failed; the issue might have been fixed.")
    sys.exit(0)
