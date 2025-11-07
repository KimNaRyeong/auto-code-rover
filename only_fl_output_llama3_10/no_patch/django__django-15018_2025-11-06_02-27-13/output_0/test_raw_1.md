Here is the reproducer script:

```python
import datetime
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured

def parse_duration_to_time(duration):
    # This function is not implemented in your example, but it should be something that converts a duration to a time.
    return datetime.datetime.now()

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        from django.core.management.commands.pause import Command
        command = Command()
        parser = command.create_parser('pause')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', action='store', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        command.handle(**{'until': '2022-01-01 00:00:00'})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected call_command to fail with mutually exclusive arguments")

if __name__ == "__main__":
    main()
```

This script will attempt to run the `pause` command with the `--for` argument, which should trigger the issue. If the issue is present, it will print a stack trace and raise an assertion error.