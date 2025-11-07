Here is the reproducer script:

```python
from django.db import IntegrityError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import CommandError
from django.conf import settings
import os
import sys

def print_stacktrace(e: Exception):
    import traceback
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
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
        from app.models import Authors, ProjectDataSet, Project, DataSet
        makemigrations_command = MakemigrationsCommand()
        makemigrations_command.execute(['app_authors'])
        
        migrate_command = MigrateCommand()
        migrate_command.execute([])
    except CommandError as e:
        print_stacktrace(e)
        raise AssertionError("Makemigrations or Migrate failed")
    
    try:
        from app.models import Authors
        Authors.objects.create(project_data_set=None, state=1, start_date='2022-01-01')
    except IntegrityError as e:
        print_stacktrace(e)
        raise AssertionError("IntegrityError occurred")

if __name__ == '__main__':
    main()
```

This script sets up a Django environment, runs the makemigrations and migrate commands for the app_authors app, creates an Authors object with invalid data (unique_together constraint), and checks if any exceptions are raised. If an exception is raised, it prints the stack trace and raises an AssertionError.