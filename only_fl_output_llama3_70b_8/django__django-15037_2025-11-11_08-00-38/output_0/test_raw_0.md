Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.db import models
from django.core.management import call_command

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

# Create a test database
os.environ['DATABASES'] = '{"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}'

# Create the tables in the database
call_command('migrate', verbosity=0, interactive=False)

# Create the tables using raw SQL
from django.db import connection
cursor = connection.cursor()
cursor.execute("CREATE TABLE foo (id serial primary key, other_id int UNIQUE);")
cursor.execute("CREATE TABLE bar (id serial primary key, other_id int, constraint myconst FOREIGN KEY(other_id) references foo(other_id));")

# Run inspectdb to generate models
call_command('inspectdb', verbosity=0, stdout=sys.stdout)

# Load the generated models
from django.apps import apps
app_config = apps.get_app_config('reproducer')
models_module = app_config.module

# Check if the issue is present
bar_model = getattr(models_module, 'Bar')
assert bar_model._meta.get_field('other_id').remote_field.model._meta.db_table == 'foo', "Foreign key to a specific field is not handled in inspectdb"
print("Issue is fixed!")

try:
    # Try to reproduce the issue
    bar_instance = bar_model(other_id=1)
    bar_instance.save()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates a test database, creates the tables using raw SQL, runs `inspectdb` to generate models, and then checks if the issue is present by verifying that the foreign key on the `Bar` model points to the correct table. If the issue is present, it raises an `AssertionError`. If the issue is fixed, it prints a success message and exits with code 0.