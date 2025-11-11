Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.core.management.color import no_style
from django.db.backends.utils import truncate_name
from django.db.models.fields.related import ForeignKey

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

def create_db_tables():
    from django.db.backends.creation import BaseDatabaseCreation
    connection = BaseDatabaseCreation('postgresql')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE foo ( id SERIAL PRIMARY KEY, other_id INT UNIQUE);")
    cursor.execute("CREATE TABLE bar (id SERIAL PRIMARY KEY, other_id INT, CONSTRAINT myconst FOREIGN KEY(other_id) REFERENCES foo(other_id));")

def test_inspectdb():
    from django.core.management import call_command
    from django.db.models.fields.related import ForeignKey

    create_db_tables()

    call_command('inspectdb', verbosity=0)

    from django.apps.registry import apps
    bar_model = apps.get_model('reproducer', 'bar')

    other_id_field = bar_model._meta.get_field('other_id')
    assert isinstance(other_id_field, ForeignKey), "other_id field is not a ForeignKey"
    assert other_id_field.to_fields == ('other_id',), "ForeignKey does not reference foo(other_id)"

try:
    test_inspectdb()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates the database tables, runs the `inspectdb` command to generate the models, and then checks if the `other_id` field in the `bar` model is a `ForeignKey` referencing `foo(other_id)`. If not, it raises an `AssertionError` with a stack trace.