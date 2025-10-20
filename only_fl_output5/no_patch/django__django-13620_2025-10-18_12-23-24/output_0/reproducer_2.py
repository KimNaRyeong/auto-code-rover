import django
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings

# Set up Django environment
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    SECRET_KEY='a_very_secret_key',
)

django.setup()

class Command(BaseCommand):
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--foo', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully called command with options: %s' % options))

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
        # Attempting to call the command with a list argument as described in the issue
        call_command('reproducer', foo=[1, 2, 3])
        print("No exception was raised. It seems the issue has been fixed.")
        # Exiting with code 0 to indicate the potential fix of the issue
        exit(0)
    except CommandError as e:
        print_stacktrace(e)
        # Raising an AssertionError since the issue is expected to be present
        raise AssertionError("The issue is still present.") from e
