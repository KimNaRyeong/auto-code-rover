import os
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.db.models import Model
from django.db.models.base import ModelBase
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    try:
        makemigrations_command = MakemigrationsCommand()
        makemigrations_command.handle('myapp')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected makemigrations to generate wrong numbered migration file")

if __name__ == '__main__':
    main()
