Here is the `reproducer.py` script to reproduce the issue:
```
```python
import os
import sys

# Create a new Django project and app
os.system("django-admin startproject repro_project")
os.chdir("repro_project")
os.system("python3 manage.py startapp app_authors")

# Create models
with open("app_authors/models.py", "w") as f:
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
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)
""")

# Make initial migrations
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py migrate")

# Change the field from foreign key to many-to-many field
with open("app_authors/models.py", "w") as f:
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
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)
""")

try:
    # Try to make migrations
    os.system("python3 manage.py makemigrations")
    os.system("python3 manage.py migrate")
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
    sys.exit(0)

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
```
This script creates a new Django project and app, defines the models, makes initial migrations, changes the field from foreign key to many-to-many field, and tries to make migrations again. If the `ValueError` exception is raised, it prints the stack trace and raises an `AssertionError`. If no exception is raised, it prints "Issue is fixed" and exits with code 0.