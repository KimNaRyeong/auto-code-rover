import os
from django.core.management import BaseCommand, call_command

def add_arguments(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--foo', nargs='+', type=int)

class Command(BaseCommand):
    def add_arguments(self, parser):
        add_arguments(parser)

    def handle(self, *args, **options):
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

if __name__ == '__main__':
    try:
        call_command('call_command_test', foo=[1, 2, 3])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
