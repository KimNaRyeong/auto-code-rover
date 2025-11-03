Here is the reproducer script:

```python
import os
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

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
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        from django.apps import apps
        from django.db.models.signals import post_migrate
        from django.db import connection

        # Create models
        settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
        settings.DATABASES['default']['NAME'] = ':memory:'
        apps.populate(['app_authors'])
        connection.close()

        try:
            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle('app_authors', [], **options)
            migrate_command = MigrateCommand()
            migrate_command.handle('app_authors', [], **options)

            # Change field project_data_set in Authors model from foreign key to many to many
            from app_authors.models import Authors, ProjectDataSet
            Authors._meta.get_field('project_data_set').remote_field = models.ManyToManyField(ProjectDataSet)
            makemigrations_command = MakemigrationsCommand()
            makemigrations_command.handle('app_authors', [], **options)
            migrate_command = MigrateCommand()
            migrate_command.handle('app_authors', [], **options)

        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")

        else:
            print("Issue fixed")
            exit(0)

if __name__ == '__main__':
    try:
        Command().handle()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script creates the models, runs makemigrations and migrate commands to reproduce the issue. If an IntegrityError is raised during the process, it prints the stack trace and raises an AssertionError.