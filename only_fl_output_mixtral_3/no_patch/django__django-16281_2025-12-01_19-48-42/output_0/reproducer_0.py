import sys
import traceback
from django.core.management import execute_from_command_line
from django.db import connection

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run():
    try:
        # Create models
        class Bar(object): pass
        class Foo(object):
            bar = models.ManyToManyField('Bar', blank=True)

        # Migrate
        execute_from_command_line(sys.argv if len(sys.argv) > 1 else ['', 'makemigrations', 'app'], exit=False)
        execute_from_command_line(sys.argv if len(sys.argv) > 1 else ['', 'migrate'], exit=False)

        # Change ManyToManyField type
        class Bar(object): pass
        class Foo(object):
            bar = models.ManyToManyField('Foo', blank=True)

        # Migrate
        execute_from_command_line(sys.argv if len(sys.argv) > 1 else ['', 'makemigrations', 'app'], exit=False)
        execute_from_command_line(sys.argv if len(sys.argv) > 1 else ['', 'migrate'], exit=False)

        # Save Foo object
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO app_foo (id, name) VALUES (1, 'test')")

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue should be present")

if __name__ == "__main__":
    run()
