Here is the reproducer script:

```python
import datetime
from django.utils.dateparse import parse_duration
from django.utils import timezone

def duration_iso_string(td):
    if td.days < 0:
        return f'-P{abs(td.days)}DT00H00M00S'
    else:
        return f'P{td.days}DT00H00M00S'

try:
    td = datetime.timedelta(days=-1)
    result = parse_duration(duration_iso_string(td))
    assert result.days == -1, "Expected days to be -1"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully.")
exit(0)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will simply print "Issue reproduced successfully." and exit with code 0.