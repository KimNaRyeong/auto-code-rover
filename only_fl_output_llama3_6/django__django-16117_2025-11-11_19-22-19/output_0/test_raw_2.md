Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.base import CommandError

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
    try:
        os.system("python manage.py startapp myapp")
        with open('models.py', 'w') as f:
            f.write('from django.db import models\n'
                    'class MyModel(models.Model):\n'
                    '    name = models.CharField(max_length=100)\n'
                    '    age = models.IntegerField()\n')
        os.system("python manage.py makemigrations myapp")
        os.system("python manage.py migrate")
        with open('models.py', 'a') as f:
            f.write('class MyModel(models.Model):\n'
                    '    name = models.CharField(max_length=100)\n'
                    '    age = models.IntegerField()\n'
                    '    class Meta:\n'
                    '        constraints = [\n'
                    '            models.CheckConstraint(\n'
                    '                check=models.Q(age__gte=1),\n'
                    '                name="Age should not be less than one"\n'
                    '            )\n'
                    '        ]\n')
        os.system("python manage.py makemigrations myapp")
        os.system("python manage.py migrate")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a new Django project, defines a model in an app, generates migrations for the model, and then runs into the issue when trying to run `makemigrations` again. If the issue is present (which should be the case), it prints the stack trace and exits with code 1. Otherwise, it exits with code 0.

Please note that you need to have Django installed in your Python environment for this script to work.