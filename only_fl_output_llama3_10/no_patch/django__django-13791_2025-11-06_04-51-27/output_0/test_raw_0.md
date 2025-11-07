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

This script defines a function `duration_iso_string` that generates an ISO 8601 duration string from a timedelta object. The reproducer function `reproduce_issue` creates a timedelta object with days=-1, converts it to an ISO 8601 duration string using the custom function, and then attempts to parse the resulting string using `parse_duration`. If the parsed result does not have days=-1, the script raises an AssertionError with a stack trace.