import sys
import os

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

# Dynamically configure Django to avoid dependency on a project's settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line

settings.configure(
    INSTALLED_APPS=[__name__],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

# Minimal Django setup
from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node, related_name='relations')

def main():
    try:
        # Apply migrations to set up the database schema in memory
        execute_from_command_line(['manage.py', 'migrate'])
        
        # To verify, we reflect the table structure directly from the database
        from django.db import connection
        with connection.cursor() as cursor:
            # Fetch the column SQL type for the M2M relation table columns
            cursor.execute(f"PRAGMA table_info('{Relation.nodes.through._meta.db_table}');")
            columns_info = {row[1]: row[2] for row in cursor.fetchall()}
            for column in ['id', 'node_id', 'relation_id']:
                assert 'bigint' in columns_info.get(column, ''), \
                    f"Column '{column}' expected to be of type 'bigint', found '{columns_info.get(column)}'"
        
        print("Test passed: M2M relation-use PositiveBigIntegerFields as expected.")
    
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
