Here is the revised `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.core.management import call_command
from django.db import models
from django.apps.config import AppConfig

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__gte=1),
                name="Age should not be.less.than.one."
            )
        ]

class MyAppConfig(AppConfig):
    name = 'myapp'
    verbose_name = "My App"

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
    import reproducer.settings as settings

    settings.INSTALLED_APPS += ['myapp']

    call_command('makemigrations', 'myapp')
    call_command('migrate')

    try:
        call_command('showmigrations', 'myapp')
    except SystemExit as e:
        if e.code != 0:
            print_stacktrace(e)
            raise AssertionError("Migration file not detected by Django")

if __name__ == '__main__':
    main()
```
This script creates a new Django app `myapp` with a model `MyModel` that has a check constraint. It then runs the `makemigrations` and `migrate` commands to create and apply the migration.

The issue is reproduced when running the `showmigrations` command, which should detect the newly generated migration file but fails to do so due to the dot in the filename.

If the issue is present, the script raises an `AssertionError` with a stack trace of the error. If the issue is fixed, the script exits with code 0.

Note that I added the line `settings.INSTALLED_APPS += ['myapp']` to configure the settings module correctly.