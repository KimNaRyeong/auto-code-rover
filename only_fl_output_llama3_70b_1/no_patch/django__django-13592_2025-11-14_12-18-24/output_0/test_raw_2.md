I apologize for the previous mistake. Here is a new `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.conf import settings
from django.db import models
from django.test.utils import get_runner

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    },
    INSTALLED_APPS=[
        'reproducer',  # Add this line
    ],
)

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

try:
    from django.db import connection
    from reproducer.models import Node, Relation  # Import the models

    # Create the tables
    from django.core.management import call_command
    call_command('makemigrations', 'reproducer')
    call_command('migrate')

    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'reproducer_relation_node'")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == 'node_id' and row[1] != 'bigint':
                raise AssertionError(f"Expected bigint type, got {row[1]}")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not present")
sys.exit(0)
```
This script creates the necessary models and database connection to reproduce the issue. It then checks the column types of the intermediate table `reproducer_relation_node` using a SQL query. If any of the columns have a type other than `bigint`, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

You need to create a `models.py` file in the same directory as this script with the following content:
```
from django.db import models
from django.contrib.gis.db import models

class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    point = models.PointField()

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node)
```
This file defines the `Node` and `Relation` models used in the script.

You can run this script by executing `python3 reproducer.py` in the root directory of your project.