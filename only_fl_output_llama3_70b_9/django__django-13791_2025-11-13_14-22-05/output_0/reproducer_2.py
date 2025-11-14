import datetime
from django.utils.dateparse import parse_duration

def duration_iso_string(td):
    if td.days < 0:
        sign = '-'
        days = -td.days
    else:
        sign = ''
        days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    microseconds = td.microseconds
    return f'P{days}DT{hours:02d}H{minutes:02d}M{seconds:02d}.{microseconds:06d}S'

def test_parse_duration_sign_ignored():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)
    assert parsed_td.days == -1, f"Expected days to be -1, but got {parsed_td.days}"

def main():
    try:
        test_parse_duration_sign_ignored()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
