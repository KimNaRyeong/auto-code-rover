Here is the reproducer script:

```python
import datetime
from django.utils import dateparse

def duration_iso_string(td):
    days = td.days
    if days < 0:
        sign = '-'
    else:
        sign = '+'

    return f'{sign}P{abs(days)}DT00H00M00S'

def reproduce_issue():
    try:
        td = datetime.timedelta(days=-1)
        duration_str = duration_iso_string(td)
        result = dateparse.parse_duration(duration_str)
        assert result.days == -1, "Expected days to be -1"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a function `duration_iso_string` that generates an ISO 8601 duration string from a timedelta object. It then uses this function to generate a duration string for a timedelta with one day, and attempts to parse it using the `dateparse.parse_duration` function.

If the parsed result does not have the expected days (-1), the script raises an AssertionError with the stack trace of the issue. If any other exception occurs during the execution, the script prints the stack trace and exits with code 1.