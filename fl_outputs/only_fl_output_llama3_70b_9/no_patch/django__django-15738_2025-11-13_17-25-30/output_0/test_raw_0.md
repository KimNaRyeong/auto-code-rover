Here is the `reproducer.py` script to reproduce the issue:
```
import os
import sys

from django.db import models
from django.apps import apps
from django.core.management import call_command

# Create a new Django project and app
os.makedirs('project', exist_ok=True)
with open('project/settings.py', 'w') as f:
    f.write("""
INSTALLED_APPS = ['app']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
""")

os.makedirs('app', exist_ok=True)
with open('app/models.py', 'w') as f:
    f.write("""
from django.db import models

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
    data_set = models.ForeignKey('DataSet', on_delete=models.PROTECT)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)
""")

# Create the initial migration
call_command('makemigrations', app_label='app')
call_command('migrate')

try:
    # Try to change the field from ForeignKey to ManyToManyField
    with open('app/models.py', 'w') as f:
        f.write("""
from django.db import models

class Authors(models.Model):
    project_data_set = models.ManyToManyField('ProjectDataSet')
    state = models.IntegerField()
    start_date = models.DateField()

class DataSet(models.Model):
    name = models.TextField(max_length=50)

class Project(models.Model):
    data_sets = models.ManyToManyField('DataSet', through='ProjectDataSet')
    name = models.TextField(max_length=50)

class ProjectDataSet(models.Model):
    data_set = models.ForeignKey('DataSet', on_delete=models.PROTECT)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)
""")

    # Try to create a new migration
    call_command('makemigrations', app_label='app')

    # This should raise an AssertionError if the issue is present
    assert len(apps.get_app_config('app').migration_module_names) == 1

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates a new Django project and app, defines the models, creates an initial migration, and then tries to change the `project_data_set` field from a ForeignKey to a ManyToManyField. If the issue is present, it should raise an AssertionError when trying to create a new migration.