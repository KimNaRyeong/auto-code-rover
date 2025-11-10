Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys

from django.db import models
from django.apps.config import AppConfig
from django.core.management import call_command

class Authors(models.Model):
    project_data_set = models.ForeignKey('ProjectDataSet', on_delete=models.PROTECT)
    state = models.IntegerField()
    start_date = models.DateField()

    class Meta:
        unique_together = (('project_data_set', 'state', 'start_date'),)

class DataSet(models.Model):
    name = models.TextField(max_length=50)

class Project(models.Model):
    data_sets = models.ManyToManyField('DataSet', through='ProjectDataSet')
    name = models.TextField(max_length=50)

class ProjectDataSet(models.Model):
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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    sys.path.append(os.getcwd())

    class MyAppConfig(AppConfig):
        name = 'myapp'
        verbose_name = 'My App'

    my_app_config = MyAppConfig

    try:
        call_command('makemigrations', verbosity=0)
        call_command('migrate', verbosity=0)

        # Change the field from ForeignKey to ManyToManyField
        Authors.project_data_set.field = models.ManyToManyField(ProjectDataSet)

        call_command('makemigrations', verbosity=0)
        call_command('migrate', verbosity=0)

    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    main()
```
This script creates the models, makes and applies migrations, then changes the `project_data_set` field from a ForeignKey to a ManyToManyField and tries to make and apply new migrations. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.

To use this script, create a new Django project and app, then add the `reproducer.py` file to the root directory of the project. Run the script using `python3 reproducer.py`.