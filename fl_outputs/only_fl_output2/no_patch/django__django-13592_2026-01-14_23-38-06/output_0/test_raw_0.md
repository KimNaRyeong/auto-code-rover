Below is a Python script named `reproducer.py` designed to reproduce the reported issue. You should place this file in the root directory of your Django project and execute it with `python3 reproducer.py`. This script attempts to create a Django model relation using `PositiveBigIntegerField` as described in your issue, and then it checks if the fields in the database match the expected types. The script will raise an `AssertionError` if the issue is present, showing the expected versus actual database field types.

```python
import os
import django
from django.core.exceptions import FieldDoesNotExist
from django.db import models, connections, DEFAULT_DB_ALIAS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Update with your project's settings module
django.setup()

class Node(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    point = models.PointField()

class Relation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nodes = models.ManyToManyField(Node, related_name='relations')

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

def check_field_type(model, field_name, expected_type):
    try:
        field_object, model, direct, m2m = model._meta.get_field_by_name(field_name)
    except AttributeError:  # For Django 2.0+
        field_object = model._meta.get_field(field_name)

    connection = connections[DEFAULT_DB_ALIAS]
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", [field_object.model._meta.db_table])
        columns_info = {row[0]: row[1] for row in cursor.fetchall()}

        actual_type = columns_info.get(field_name)
        assert actual_type == expected_type, f"Field type for '{field_name}' is '{actual_type}', expected '{expected_type}'"

def main():
    try:
        # The following line ensures that the table for Relation is created.
        Relation.objects.all().delete()

        intermediary_model = Relation._meta.get_field('nodes').remote_field.through
        check_field_type(intermediary_model, 'id', 'bigint')  # Check if the 'id' field is 'bigint'
        check_field_type(intermediary_model, 'node_id', 'bigint')  # Check if the 'node_id' field is 'bigint'
        check_field_type(intermediary_model, 'relation_id', 'bigint')  # Check if the 'relation_id' field is 'bigint'
        
        print("Issue not present, exiting with code 0.")
        exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

Make sure to replace `'your_project.settings'` with the actual settings module of your Django project. This script forces model table creation and then checks the types of specific fields within the many-to-many intermediary table. If the types do not match the expected 'bigint', as per the PostgreSQL `PositiveBigIntegerField` expectation, an `AssertionError` will be raised with a detailed stack trace.