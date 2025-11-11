Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.db.models.signals import post_migrate
from django.core.management.commands.makemigrations import CommandError
from django.core.management import call_command
from django.conf import settings
from django.apps import apps

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

def reproduce_issue():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    django.setup()

    class AppVersion(models.Model):
        name = models.CharField(max_length=10, primary_key=True)

    class Vulnerability(models.Model):
        cve_id = models.CharField(max_length=15, primary_key=True)
        app = models.ManyToManyField(AppVersion)

    try:
        from test_project.models import Vulnerability

        original_max_length = Vulnerability._meta.get_field('cve_id').max_length
        new_max_length = 100

        operations = [
            migrations.AlterField(
                model_name='vulnerability',
                name='cve_id',
                field=models.CharField(max_length=new_max_length, primary_key=True, serialize=False),
            ),
        ]

        call_command('makemigrations', 'test_app')
        call_command('migrate')

        cursor = settings.DATABASES['default']['cursor']
        cursor.execute("SELECT * FROM test_app_vulnerability_app")
        result = cursor.fetchall()

        if len(result) > 0:
            raise AssertionError("Expected no rows in the table, but got {}".format(len(result)))
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a test Django project with two models: `AppVersion` and `Vulnerability`. The `Vulnerability` model has a many-to-many field to `AppVersion`. Then it runs the makemigrations command for this app, which should create the necessary database tables. Finally, it checks if there are any rows in the table that was created by the many-to-many field. If there are, it raises an AssertionError and prints the stack trace.