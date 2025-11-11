import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command

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
    class Command(BaseCommand):
        def add_arguments(self, parser):
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument('--foo', nargs='+', type=int)

        def handle(self, *args, **options):
            pass

    try:
        command = Command()
        command.add_arguments(sys.argv)
        call_command('call_command_test', foo=[1, 2, 3])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
