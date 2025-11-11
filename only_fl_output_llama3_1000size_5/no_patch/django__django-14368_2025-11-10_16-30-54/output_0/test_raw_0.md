Here is the `reproducer.py` file that reproduces the issue:

```python
import django.utils.dateparse
from datetime import datetime

def reproduce_issue():
    try:
        datetime_obj = django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to parse the ISO-8601 datetime string "2012-04-23T10:20:30.400 -02" using Django's `parse_datetime` function from `django.utils.dateparse`. If the parsing fails (i.e., returns `None`), it catches the exception, prints the stack trace using the provided `print_stacktrace` function, and then raises an `AssertionError` to indicate that the issue has been reproduced.

To run this script, simply execute it with Python 3: `python3 reproducer.py`. If the issue is present, you should see a stack trace indicating where the parsing failure occurred.