Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration

def duration_iso_string(td):
    if td.days < 0:
        return f'-P{abs(td.days)}DT00H00M00S'
    else:
        return f'P{td.days}DT00H00M00S'

def reproduce_issue():
    try:
        td = datetime.timedelta(days=-1)
        iso_str = duration_iso_string(td)
        result = parse_duration(iso_str)
        assert result.days == -1, "Expected days to be -1"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a timedelta object with one day and then converts it to an ISO string using the `duration_iso_string` function. It then attempts to parse this string back into a timedelta object using the `parse_duration` function. If the parsed result has days that are not -1, the script prints the stack trace of the issue and raises an AssertionError.