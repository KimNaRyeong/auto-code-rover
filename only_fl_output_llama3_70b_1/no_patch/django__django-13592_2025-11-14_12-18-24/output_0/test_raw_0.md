Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.conf import settings
from django.db import models
from django.test.utils import get_runner

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.gis',
    ],
)

class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    point = models.PointField()

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node)

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
    from django.db.backends.utils import create_connection
    conn = create_connection(settings.DATABASES['default'])
    cursor = conn.cursor()
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'relation_node'")
    rows = cursor.fetchall()
    for row in rows:
        if row[1] != 'bigint':
            raise AssertionError(f"Expected bigint type, got {row[1]}")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not present")
sys.exit(0)
```
This script creates the necessary models and database connection to reproduce the issue. It then checks the column types of the intermediate table `relation_node` using a SQL query. If any of the columns have a type other than `bigint`, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

You can run this script by executing `python3 reproducer.py` in the root directory of your project.