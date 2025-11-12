Here is the reproducer script in a code block:

```python
import django.utils.dateparse
from datetime import datetime

def reproduce_issue():
    try:
        dt = django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
        assert dt is not None, "Expected valid datetime"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to parse the given ISO-8601 datetime string using Django's `dateparse` module. If the parsing fails and returns `None`, it prints a stack trace of the issue and exits with code 0.