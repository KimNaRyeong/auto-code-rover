Here is the reproducer script:

```python
import os
from django.db import IntegrityError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
        from project.models import Authors, ProjectDataSet, Project, DataSet

        # Create initial migrations
        makemigrations_command = MakemigrationsCommand()
        makemigrations_command.handle('app_authors')

        # Change the field in Authors model to ManyToManyField
        with open('models.py', 'r') as f:
            models_content = f.read()

        models_content = models_content.replace(
            "project_data_set = models.ForeignKey(\n"
            "    ProjectDataSet,\n"
            "    on_delete=models.PROTECT\n"
            ")",
            "project_data_set = models.ManyToManyField(\n"
            "    ProjectDataSet,\n"
            ")"
        )

        with open('models.py', 'w') as f:
            f.write(models_content)

        # Migrate the database
        migrate_command = MigrateCommand()
        try:
            migrate_command.handle()
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError("Expected IntegrityError")

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

if __name__ == "__main__":
    Command().handle()
```

This script sets up a Django project, creates the initial migrations for the `app_authors` app, changes the field in the `Authors` model from ForeignKey to ManyToManyField, and then attempts to run the migrations. If an `IntegrityError` is raised during this process, it prints the stack trace and raises an `AssertionError`.