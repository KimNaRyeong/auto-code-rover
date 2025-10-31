Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration

def duration_iso_string(td):
    days = td.days
    if days < 0:
        sign = '-'
    else:
        sign = 'P'

    if abs(days) > 1:
        return f'{sign}P{abs(days)}D00H00M00S'
    elif abs(days) == 1:
        return f'{sign}P1D00H00M00S'
    else:
        return f'{sign}P0D00H00M00S'

def main():
    td = datetime.timedelta(days=-1)
    iso_str = duration_iso_string(td)
    try:
        parsed_td = parse_duration(iso_str)
        if parsed_td is None:
            print_stacktrace(AssertionError("parse_duration returned None"))
            raise
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will run the `parse_duration` function with a timedelta string that only contains days. If the issue is present and the parsed timedelta is None, it will print the stack trace and raise an AssertionError.