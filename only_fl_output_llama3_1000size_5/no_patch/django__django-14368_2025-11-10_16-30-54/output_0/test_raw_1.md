Here is the `reproducer.py` file that reproduces the issue:

```python
import django.utils.dateparse

def reproduce_issue():
    try:
        datetime_obj = django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
        assert datetime_obj is not None, "Issue reproduced"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to parse the ISO-8601 datetime string "2012-04-23T10:20:30.400 -02" using Django's `parse_datetime` function from `django.utils.dateparse`. If the parsing fails (i.e., returns `None`), it raises an `AssertionError` with a message indicating that the issue has been reproduced, and prints the stack trace using the provided `print_stacktrace` function.