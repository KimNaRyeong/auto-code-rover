Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration
from django.utils.dateformat import duration_iso_string

def reproduce_issue():
    td = datetime.timedelta(days=-1)
    iso_str = duration_iso_string(td)
    try:
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