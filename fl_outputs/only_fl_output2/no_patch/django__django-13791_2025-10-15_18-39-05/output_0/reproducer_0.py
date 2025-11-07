# reproducer.py
from datetime import timedelta
from django.utils.dateparse import parse_duration
from django.core.exceptions import ValidationError

def duration_iso_string(td):
    """
    Converts a timedelta object into its ISO 8601 string representation.
    This function assumes a simple case for demonstration and may not cover all ISO 8601 nuances.
    """
    days = td.days
    seconds = td.seconds
    microseconds = td.microseconds

    sign = "-" if days < 0 or (days == 0 and seconds < 0) or (days == 0 and seconds == 0 and microseconds < 0) else ""
    days_part = f"{abs(days)}D" if days != 0 else ""
    time_part = "T"

    hours, remainder = divmod(abs(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    hours_part = f"{hours}H" if hours else ""
    minutes_part = f"{minutes}M" if minutes else ""
    seconds_part = f"{seconds}.{microseconds:06}S" if microseconds else f"{seconds}S" if seconds else ""

    if not (hours_part or minutes_part or seconds_part):
        time_part = ""  # No time component

    iso_string = f"{sign}P{days_part}{time_part}{hours_part}{minutes_part}{seconds_part}"
    return iso_string

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

def test_parse_duration_with_days():
    td_negative_days = timedelta(days=-1)
    duration_str_negative_days = duration_iso_string(td_negative_days)
    parsed_duration_negative_days = parse_duration(duration_str_negative_days)

    try:
        assert parsed_duration_negative_days == td_negative_days, "parse_duration should correctly handle negative days"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    td_negative_days_microseconds = timedelta(days=-1, microseconds=1)
    duration_str_negative_days_microseconds = duration_iso_string(td_negative_days_microseconds)
    parsed_duration_negative_days_microseconds = parse_duration(duration_str_negative_days_microseconds)

    try:
        assert parsed_duration_negative_days_microseconds == td_negative_days_microseconds, "parse_duration should correctly handle negative days with positive microseconds"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_parse_duration_with_days()
        print("Issue not present, the test passed successfully.")
    except AssertionError:
        print("Test failed, the issue is present.")
        exit(1)
