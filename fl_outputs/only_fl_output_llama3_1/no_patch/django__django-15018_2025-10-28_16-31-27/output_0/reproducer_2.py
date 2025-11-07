import datetime
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.core.management.base import CommandError

def parse_duration_to_time(duration):
    # This function should be implemented to convert duration into time
    pass

def parse_time(time):
    # This function should be implemented to parse time
    pass

class Command:
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', action='store', type=parse_time)

    def handle(self, until: datetime, **_):
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

def main():
    try:
        call_command(Command(), 'pause')
    except (CommandError, ValidationError) as e:
        print_stacktrace(e)
        raise AssertionError("Expected mutually exclusive arguments to fail")

if __name__ == "__main__":
    main()
