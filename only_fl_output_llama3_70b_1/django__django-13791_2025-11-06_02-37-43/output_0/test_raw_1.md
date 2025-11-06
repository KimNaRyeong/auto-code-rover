Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
import datetime
from iso8601 import timedelta

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
    return f'{sign}P{days}DT{hours:02d}H{minutes:02d}M{seconds:02d}.{microseconds:06d}S'

def test_parse_duration_sign_ignored():
    def parse_duration(iso_string):
        days = 0
        sign = 1
        for char in iso_string:
            if char == '-':
                sign = -1
            elif char.isdigit():
                days = int(char)
        return datetime.timedelta(days=sign * days)

    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    try:
        assert parsed_td.days == -1
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

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
    test_parse_duration_sign_ignored()
```
This script defines its own `duration_iso_string` and `parse_duration` functions to reproduce the issue, since the original ones are part of Django.