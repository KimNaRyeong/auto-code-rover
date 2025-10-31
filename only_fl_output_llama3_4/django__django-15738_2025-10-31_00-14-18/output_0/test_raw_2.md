Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import BaseCommand
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

class Command(BaseCommand):
    help = 'Reproduce the issue'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
        from django.conf import settings
        from app.models import Authors, ProjectDataSet, DataSet, Project

        try:
            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle(args=['app'], verbosity=0)

            migrate_command = MigrateCommand()
            migrate_command.handle(verbosity=0)
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError('Issue reproduced')

        try:
            Authors._meta.unique_together = [('project_data_set', 'state', 'start_date'),]
            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle(args=['app'], verbosity=0)

            migrate_command = MigrateCommand()
            migrate_command.handle(verbosity=0)
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError('Issue reproduced')

if __name__ == '__main__':
    try:
        Command().handle()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

Please note that you need to replace `'app'` with the actual name of your Django app in the `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')` line.