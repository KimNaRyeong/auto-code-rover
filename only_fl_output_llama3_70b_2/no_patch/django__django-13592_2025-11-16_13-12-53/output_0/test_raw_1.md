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
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
)

class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node)

def print_stacktrace(e: Exception):
    import traceback
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
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'relation_node'")
        columns = cursor.fetchall()

        for column in columns:
            if column[0] == 'node_id' and column[1] != 'bigint':
                raise AssertionError("PositiveBigIntegerField is not respected in m2m intermediate table")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates the necessary models, sets up a test database connection, and checks if the `node_id` column in the `relation_node` table has the correct data type (`bigint`). If not, it raises an `AssertionError` with a stack trace.