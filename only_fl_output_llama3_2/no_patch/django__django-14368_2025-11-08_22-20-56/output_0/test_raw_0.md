Here is the reproducer script:

```python
import django.utils.dateparse
from datetime import datetime

def reproduce_issue():
    try:
        datetime.fromisoformat('2012-04-23T10:20:30.400 -02')
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to parse the ISO-8601 datetime string '2012-04-23T10:20:30.400 -02' using `datetime.fromisoformat()`. If the parsing fails, it prints a stack trace and raises an `AssertionError` to indicate that the issue is present.