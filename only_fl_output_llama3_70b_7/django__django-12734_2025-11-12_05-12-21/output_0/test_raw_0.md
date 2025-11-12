Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys

from django.db import models
from django.apps import apps
from django.core.management import call_command
from django.test.utils import get_runner

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

# Create a new Django project
os.system("django-admin startproject reproducer_project")
os.chdir("reproducer_project")

# Create a new app
os.system("python manage.py startapp myapp")

# Define the models
with open("myapp/models.py", "w") as f:
    f.write("""
from django.db import models

class AppVersion(models.Model):
    pass

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=15, primary_key=True)
    app = models.ManyToManyField(AppVersion)
""")

# Make migrations
os.system("python manage.py makemigrations myapp")
os.system("python manage.py migrate")

# Change the max length of cve_id and make a new migration
with open("myapp/models.py", "w") as f:
    f.write("""
from django.db import models

class AppVersion(models.Model):
    pass

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=100, primary_key=True)
    app = models.ManyToManyField(AppVersion)
""")
os.system("python manage.py makemigrations myapp")

# Apply the migration
os.system("python manage.py migrate")

# Check if the issue is present
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT character_maximum_length FROM information_schema.columns WHERE table_name='myapp_vulnerability_app' AND column_name='vulnerability_id';")
result = cursor.fetchone()[0]

if result != 100:
    raise AssertionError("Issue is present: vulnerability_id field length in table myapp_vulnerability_app remains unchanged")

print("Issue is fixed!")
sys.exit(0)
```
This script creates a new Django project, defines the models, makes migrations, changes the max length of `cve_id`, and applies the migration. Then it checks if the issue is present by querying the database to get the maximum length of the `vulnerability_id` field in the `myapp_vulnerability_app` table. If the length is not 100, it raises an `AssertionError` with a stack trace. If the length is 100, it prints "Issue is fixed!" and exits with code 0.