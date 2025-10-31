Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration
from django.utils.dateformat import duration_iso_string

def main():
    td = datetime.timedelta(days=-1)
    iso_str = duration_iso_string(td)
    try:
        parsed_td = parse_duration(iso_str)
        assert parsed_td.days == -1, "Expected days to be -1"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will run the `parse_duration` function with a timedelta string that only contains days. If the issue is present and the parsed timedelta has days equal to 1 instead of -1, it will print the stack trace and raise an AssertionError.