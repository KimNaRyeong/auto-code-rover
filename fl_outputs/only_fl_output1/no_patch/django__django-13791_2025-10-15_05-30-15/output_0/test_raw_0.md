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

def duration_iso_string(td):
    """
    Convert timedelta to ISO 8601 duration string.
    This is a simple utility function to convert Python timedelta objects
    into ISO 8601 duration strings. This implementation is limited and does not
    cover the full range of ISO 8601, but it is sufficient for the purpose of this
    demonstration.
    """
    seconds = int(td.total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    sign = "-" if td.total_seconds() < 0 else ""
    return f'{sign}P{abs(days)}DT{abs(hours)}H{abs(minutes)}M{abs(seconds)}S'

def main():
    from django.utils.dateparse import parse_duration
    from datetime import timedelta
    try:
        # Create a timedelta with -1 day.
        td = timedelta(days=-1)
        # Convert the timedelta to an ISO 8601 duration string.
        iso_duration_str = duration_iso_string(td)
        assert iso_duration_str == '-P1DT0H0M0S', "The ISO string representation is incorrect."
        # Parse the ISO duration string back to a timedelta object.
        parsed_td = parse_duration(iso_duration_str)
        # The parsed timedelta should also represent -1 day.
        assert parsed_td == timedelta(days=-1), "The parsed timedelta does not match the original."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issue detected.")
    exit(0)

if __name__ == "__main__":
    main()
```