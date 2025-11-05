import datetime
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured

def parse_duration_to_time(duration):
    # This function is not implemented in your example, but it should return a datetime object
    pass

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

def reproduce_issue():
    try:
        class Command(BaseCommand):
            def add_arguments(self, parser) -> None:
                group = parser.add_mutually_exclusive_group(required=True)
                group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
                group.add_argument('--until', action='store', type=parse_time)

            def handle(self, until: datetime, **_):
                pass

        call_command(Command(), 'pause', '--for', 'now', '--until', '2022-01-01')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
