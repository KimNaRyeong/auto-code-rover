Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_datetime

def reproduce_issue():
    try:
        datetime_obj = parse_datetime("2012-04-23T10:20:30.400 -02")
        assert datetime_obj is not None, "Expected a valid datetime object"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to parse the given ISO-8601 datetime string using Django's `parse_datetime` function. If the parsing fails (i.e., returns `None`) due to the presence of whitespace characters between the time strings and timezone strings, it will print a stack trace and exit with code 0 when the issue is fixed.

You can run this script by executing `python3 reproducer.py`.