Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError, ProgrammingError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import CommandError

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

django.setup()

class Authors(models.Model):
    project_data_set = models.ForeignKey(
        'ProjectDataSet',
        on_delete=models.PROTECT
    )
    state = models.IntegerField()
    start_date = models.DateField()

    class Meta:
        unique_together = (('project_data_set', 'state', 'start_date'),)

class DataSet(models.Model):
    name = models.TextField(max_length=50)

class Project(models.Model):
    data_sets = models.ManyToManyField(
        DataSet,
        through='ProjectDataSet',
    )
    name = models.TextField(max_length=50)

class ProjectDataSet(models.Model):
    """
    Cross table of data set and project
    """
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)

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
        makemigrations_command = MakemigrationsCommand()
        makemigrations_command.handle(app_label='app_authors', verbosity=0)
    except (IntegrityError, ProgrammingError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

    try:
        migrate_command = MigrateCommand()
        migrate_command.handle(verbosity=0)
    except (IntegrityError, ProgrammingError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")
```

This script sets up a Django project with the given models and runs the makemigrations and migrate commands. If any IntegrityError or ProgrammingError exceptions are raised during these operations, it prints the stack trace and raises an AssertionError with the message "Issue present".