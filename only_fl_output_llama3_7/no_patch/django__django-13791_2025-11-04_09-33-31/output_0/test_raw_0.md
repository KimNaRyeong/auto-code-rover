Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration
import sys

def duration_iso_string(td):
    if td.days < 0:
        return f'-P{abs(td.days)}DT00H00M00S'
    else:
        return f'P{td.days}DT00H00M00S'

try:
    td = datetime.timedelta(days=-1)
    result = parse_duration(duration_iso_string(td))
    if result.days != -1:
        raise AssertionError("Expected days to be -1, but got {}".format(result.days))
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not present. Exiting with code 0.")
sys.exit(0)
```

This script will run the `parse_duration` function with a timedelta string that only contains days and check if the result's days are -1. If they're not, it will raise an AssertionError and print the stack trace.