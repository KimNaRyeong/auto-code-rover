import os
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import StateApps
from django.core.management.commands.makemigrations import CommandError

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    from django.core.management import execute_from_command_line
    try:
        models.Model._meta.db_table = "new_table"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Migrations drops explicit primary key defined on a model when it's altered.")
    else:
        os._exit(0)

if __name__ == "__main__":
    main()
