import os
import sys
from django.core.management import execute_from_command_line
from django.db.models import Model, ManyToManyField
from django.db import models
from django.db.migrations.operations.models import RenameModel
from django.db.migrations.state import StateApps
from django.conf import settings

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
    settings.configure()
    try:
        from edemo.vault.models import Incident
        from edemo.incidents.models import Incident as Incidents

        apps = StateApps(settings)
        operations = [
            migrations.RenameModel(
                old_name='Incident',
                new_name='Folder',
            ),
        ]
        execute_from_command_line(['manage.py', 'migrate'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
