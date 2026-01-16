Certainly! Here's a standalone Python script named `reproducer.py` that demonstrates the issue described. Make sure to adjust paths as necessary if you're running this script in a specific environment or if the Django project structure differs from the defaults.

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
    test_string = '2012-04-23T10:20:30.400 -02'
    try:
        result = parse_datetime(test_string)
        assert result is not None, "parse_datetime returned None for a valid ISO-8601 datetime string with space before timezone."
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        # Assuming Django environment is correctly set up and this script is running in the correct context
        import django
        django.setup()

        test_parse_datetime_with_space()
        print("Test completed successfully - the issue is fixed.")
        sys.exit(0)  # Exit code 0 to indicate success
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate failure due to AssertionError
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate a generic failure
```

This script checks whether Django's `parse_datetime` function correctly parses ISO-8601 datetime strings that contain a space before the timezone. It specifically asserts that the result of parsing such a string should not be `None`. If the issue is present, it will raise an `AssertionError` and print a stack trace. When Django's `parse_datetime` function is correctly able to parse the datetime string with a space before the timezone, the script will exit with code 0, indicating the issue is fixed.

**Note:** This script assumes that you have Django installed and properly configured in your environment. If you're running this in a Django project, make sure your `DJANGO_SETTINGS_MODULE` is correctly set. For standalone testing outside a project, ensure Django is installed and configured manually if necessary.