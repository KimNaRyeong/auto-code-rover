The issue seems to be related to the GDAL library not being installed or properly configured. Here is a revised reproducer script that does not import the `django.contrib.gis` module:

```python
import os
from django.db import models

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

class Command:
    help = 'Reproduce the issue'

    def handle(self, *args, **options):
        try:
            class Node(models.Model):
                id = models.PositiveBigIntegerField(primary_key=True)
                point = None

            class Relation(models.Model):
                id = models.PositiveBigIntegerField(primary_key=True)
                nodes = models.ManyToManyField(Node)

            os.system('python manage.py makemigrations')
            os.system('python manage.py migrate')

        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    Command().handle()
```

This script creates the `Node` and `Relation` models with a Many-To-Many relationship, then attempts to create the database tables using Django's migration system. If an exception is raised during this process (which should happen if the issue is present), it prints the stack trace and raises the exception again.

Please note that you need to have a Django project set up in your environment for this script to work correctly.