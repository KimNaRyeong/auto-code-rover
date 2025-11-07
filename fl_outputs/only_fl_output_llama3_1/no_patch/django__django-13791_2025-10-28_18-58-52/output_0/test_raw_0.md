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
        duration_str = duration_iso_string(td)
        result = parse_duration(duration_str)
        assert result.days == -1, "Expected days to be -1"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script defines a function `duration_iso_string` that converts a timedelta object into an ISO 8601 duration string. It then calls the `parse_duration` function from Django's dateparse module with this string and checks if the resulting timedelta has the expected days value of -1. If not, it prints the stack trace using the provided `print_stacktrace` function and raises an AssertionError.