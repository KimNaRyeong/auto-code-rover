import datetime
from django.utils.dateparse import parse_duration

def duration_iso_string(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    sign = '-' if days < 0 else ''
    return f'{sign}P{abs(days)}DT{hours:02}H{minutes:02}M{seconds:02}S'

def test_parse_duration():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    assert parsed_td.days == -1, f"Expected days to be -1, but got {parsed_td.days}"

try:
    test_parse_duration()
except AssertionError as e:
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
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
