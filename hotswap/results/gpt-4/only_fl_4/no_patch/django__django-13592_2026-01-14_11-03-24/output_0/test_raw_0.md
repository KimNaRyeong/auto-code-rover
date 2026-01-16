```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models


# Define a minimal Django configuration for running this script
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'dbname',
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    },
    INSTALLED_APPS=('__main__',),
    SECRET_KEY='django-insecure-reproducer',
    USE_TZ=True,
)

django.setup()


# Define models to reproduce the issue
class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    point = models.PointField()


class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node, related_name='relations')


# Function to print the stack trace, as requested
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


# Main function to perform the verification
def main():
    try:
        # Set up the database table
        execute_from_command_line(['manage.py', 'migrate'])

        # Introspect the database to find the type of the 'id' columns of the relation table
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
            """, [Relation.nodes.through._meta.db_table])
            column_types = dict(cursor.fetchall())

        # Verify the types of the 'relation_id' and 'node_id' columns
        assert column_types.get('relation_id') == 'bigint', f"relation_id type is {column_types.get('relation_id')}, expected bigint"
        assert column_types.get('node_id') == 'bigint', f"node_id type is {column_types.get('node_id')}, expected bigint"

        print("Issue not present.")

    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
```

In this script:

- A minimal Django project configuration is setup, including a setting for a PostgreSQL database, which is required to reproduce this issue. You need to adjust the `DATABASES` settings with your actual database credentials.
  
- Two models, `Node` and `Relation`, are defined to mimic the given scenario with a `ManyToManyField` and a `PositiveBigIntegerField`.

- The script then creates the necessary database tables and checks the type of `relation_id` and `node_id` columns in the automatically generated through table for the `ManyToManyField` relation between `Node` and `Relation`. It expects these column types to be `bigint`, reflecting the use of `PositiveBigIntegerField`.

- Please remember to adjust the database settings in the script and ensure that Django is installed in the environment where this script will be executed.