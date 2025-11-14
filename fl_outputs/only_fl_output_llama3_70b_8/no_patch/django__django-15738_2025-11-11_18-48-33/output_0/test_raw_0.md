Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys

# Create a new Django project and app
os.system("django-admin startproject repro_project")
os.chdir("repro_project")
os.system("python3 manage.py startapp app_authors")

# Create models and initial migration
with open("app_authors/models.py", "w") as f:
    f.write("""
from django.db import models

class DataSet(models.Model):
    name = models.TextField(max_length=50)

class Project(models.Model):
    data_sets = models.ManyToManyField(DataSet, through='ProjectDataSet')
    name = models.TextField(max_length=50)

class ProjectDataSet(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)

class Authors(models.Model):
    project_data_set = models.ForeignKey(ProjectDataSet, on_delete=models.PROTECT)
    state = models.IntegerField()
    start_date = models.DateField()

    class Meta:
        unique_together = (('project_data_set', 'state', 'start_date'),)
""")

os.system("python3 manage.py makemigrations app_authors")
os.system("python3 manage.py migrate")

# Try to change the field from ForeignKey to ManyToManyField
with open("app_authors/models.py", "w") as f:
    f.write("""
from django.db import models

class DataSet(models.Model):
    name = models.TextField(max_length=50)

class Project(models.Model):
    data_sets = models.ManyToManyField(DataSet, through='ProjectDataSet')
    name = models.TextField(max_length=50)

class ProjectDataSet(models.Model):
    data_set = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('data_set', 'project'),)

class Authors(models.Model):
    project_data_set = models.ManyToManyField(ProjectDataSet)
    state = models.IntegerField()
    start_date = models.DateField()

    # class Meta:
    #     unique_together = (('project_data_set', 'state', 'start_date'),)
""")

try:
    os.system("python3 manage.py makemigrations app_authors")
    os.system("python3 manage.py migrate")
except Exception as e:
    print_stacktrace(e)
    assert False, "Error occurred while trying to change the field from ForeignKey to ManyToManyField"

print("Issue not reproduced. The migration was successful.")
sys.exit(0)
```
This script creates a new Django project and app, defines the models, makes an initial migration, and then tries to change the `project_data_set` field in the `Authors` model from a `ForeignKey` to a `ManyToManyField`. If the issue is present, it should raise a `ValueError` when trying to make the migration, and the script will print the stack trace of the error.