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

This script defines a `duration_iso_string` function that generates an ISO 8601 duration string for a given timedelta. The `reproduce_issue` function uses this function to generate the input string, then calls `parse_duration` with the generated string and asserts that the result has the expected days value of -1. If the assertion fails, it prints the stack trace using the provided `print_stacktrace` function and raises an AssertionError.