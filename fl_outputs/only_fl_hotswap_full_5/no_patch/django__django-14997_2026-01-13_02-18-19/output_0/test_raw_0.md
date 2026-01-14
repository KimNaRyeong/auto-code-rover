 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management.base import BaseCommand
from django.db import connections, migrations
from django.db.backends.utils import DatabaseWrapper
from django.db.backends.sqlite3.base import SQLite3Wrapper
from django.db.migrations.operations.fields import AlterField
from django.db.migrations.migration import Migration

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ReproducerCommand(BaseCommand):
    help = "Reproduce the SQLite unique constraint issue"

    def handle(self, *args, **options):
        connection = connections['default']
        if not isinstance(connection.vendor, SQLite3Wrapper):
            print("This command only works with SQLite3.", file=sys.stderr)
            sys.exit(1)

        database = connection.settings_dict['NAME']
        with connections.schema_editor() as schema_editor:
            # Create the initial migration
            schema_editor.create_model(
                'Tag',
                fields=[
                    ('id', migrations.AutoField(primary_key=True)),
                    ('name', migrations.SlugField()),
                    ('value', migrations.CharField(max_length=200)),
                ],
                options={'ordering': ['name', 'value']},
            )
            schema_editor.add_constraint(
                'Tag',
                migrations.UniqueConstraint(
                    fields=['name', 'value'],
                    name='unique_name_value',
                ),
            )

            # Apply the initial migration
            applied = []
            for migration in migrations.revision.app_migrations(database):
                if migration.applied:
                    applied.append(migration.name)
            if '0001_initial' not in applied:
                schema_editor.migrate(
                    [Migration(database, 'myapp', '0001_initial')],
                    fake=False,
                )

            # Create the second migration
            class Migration(migrations.Migration):
                dependencies = [
                    ('myapp', '0001_initial'),
                ]
                operations = [
                    AlterField(
                        model_name='Tag',
                        name='value',
                        field=migrations.CharField(max_length=150),
                    ),
                ]
            schema_editor.migrate(
                [Migration(database, 'myapp', '0002_alter_tag_value')],
                fake=False,
            )

if __name__ == "__main__":
    try:
        ReproducerCommand().handle(*sys.argv[1:])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, create a new Django project, add a new app, and replace the contents of the `manage.py` file with the above script. Then, run the following commands:
```
python3 manage.py makemigrations myapp
python3 manage.py migrate
```
The script should print the stack trace of the issue and exit with code 1.

To fix the issue, modify the `max_length` argument of the `value` field in the `Tag` model to 200, and then run the following commands:
```
python3 manage.py makemigrations myapp
python3 manage.py migrate
```
The script should exit with code 0, indicating that the issue has been fixed.