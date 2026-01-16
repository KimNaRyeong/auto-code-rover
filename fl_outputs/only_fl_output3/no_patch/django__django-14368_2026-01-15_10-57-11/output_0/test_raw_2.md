Given the goal to replicate the issue where Django does not support space separators in ISO-8601 datetime strings between the time and timezone as reported, we will leverage Django's `django.utils.dateparse.parse_datetime` directly for this task. This approach requires Django to be installed but does not require a full Django project setup.

Below is the standalone Python file named `reproducer.py` that you should put in the root directory of your project and execute with `python3 reproduducer.py`. Ensure that Django is installed in your environment.

```python
# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_parse_datetime_with_space():
    from django.utils.dateparse import parse_datetime
    test_datetime_string = '2012-04-23T10:20:30.400 -02'
    parsed_datetime = parse_datetime(test_datetime_string)
    try:
        assert parsed_datetime is not None, "Failed to parse ISO-8601 datetime string with space before timezone."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_parse_datetime_with_space()
        print("Test passed: Issue seems to be resolved")
        sys.exit(0)  # 0 indicates the issue described is not present
    except AssertionError:
        sys.exit(1)  # Non-zero exit code indicates the script caught the issue
```

This script directly attempts to reproduce the specified issue by attempting to parse an ISO-8601 datetime string that includes a space separator before the timezone offset—a specification that Django's `parse_datetime` might not handle correctly, according to the issue description. The script uses an assertion to check whether the function fails to return a datetime object, capturing the exact nature of the reported issue. If the assertion fails (i.e., `parse_datetime` returns `None`), the script raises an `AssertionError` and prints a detailed traceback of where the error occurred, fulfilling the requirement to illustrate the presence of this issue. The script exits with code `0` if the issue is fixed/resolved (meaning `parse_datetime` parses the string successfully) and exits with a non-zero code (`1` in this case) if the assertion fails, indicating the issue is still present.