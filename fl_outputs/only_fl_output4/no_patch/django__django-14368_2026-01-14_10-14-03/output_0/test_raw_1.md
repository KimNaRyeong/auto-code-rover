```python
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

def test_parse_datetime_with_space():
    from django.utils.dateparse import parse_datetime
    
    # Correctly formatted string without space between time and timezone
    dt1 = parse_datetime('2012-04-23T10:20:30.400-02')
    assert dt1 is not None, "Failed to parse correctly formatted datetime without space"
    
    # Correctly formatted string with space between time and timezone
    dt2 = parse_datetime('2012-04-23T10:20:30.400 -02')
    
    # Should raise an AssertionError if dt2 is None (issue exists)
    assert dt2 is not None, "Failed to parse correctly formatted datetime with space"

if __name__ == "__main__":
    try:
        test_parse_datetime_with_space()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    print("Issue resolved, exiting with code 0.")
    raise SystemExit(0)
```

This script is designed to be executed in a Django project environment where `django.utils.dateparse.parse_datetime` is available. It tests the parsing of ISO-8601 datetime strings both with and without a space between the time and timezone component. The script uses `assert` statements to verify correct behavior; if an assertion fails, it prints a stack trace of the issue highlighting the failure point. If the issue described is present, the script will raise an `AssertionError` and print a stack trace specific to where the assertion failed. Once the issue is resolved and both datetime strings are parsed correctly, the script exits with code `0`, indicating success.