 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management.base import BaseCommand
from django.db import connections, migrations
from django.db.backends.utils import DatabaseWrapper
from django.db.backends.sqlite3.base import SQLiteDatabaseWrapper
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
        # Connect to the database
        connection = connections['default']
        if not isinstance(connection.wrapper, SQLiteDatabaseWrapper):
            print("This reproducer only works with SQLite.", file=sys.stderr)
            sys.exit(1)

        # Create the initial migration
        initial_migration = Migration(
            "myapp",
            "0001_initial",
            dependencies=[],
            operations=[
                migrations.CreateModel(
                    name='Tag',
                    fields=[
                        ('id', migrations.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', migrations.SlugField(help_text='The tag key.')),
                        ('value', migrations.CharField(help_text='The tag value.', max_length=200)),
                    ],
                    options={
                        'ordering': ['name', 'value'],
                    },
                ),
                migrations.AddConstraint(
                    model_name='tag',
                    constraint=migrations.UniqueConstraint(migrations.expressions.F('name'), migrations.expressions.F('value'), name='unique_name_value'),
                ),
            ],
        )

        # Apply the initial migration
        migrations.migrate('myapp', initial_migration, connection)

        # Create the second migration
        alter_migration = Migration(
            "myapp",
            "0002_alter_tag_value",
            dependencies=['myapp.0001_initial'],
            operations=[
                AlterField(
                    model_name='tag',
                    name='value',
                    field=migrations.CharField(help_text='The tag value.', max_length=150),
                ),
            ],
        )

        # Apply the second migration
        try:
            migrations.migrate('myapp', alter_migration, connection)
        except Exception as e:
            print_stacktrace(e)
            assert False, "The issue should be reproduced here"

if __name__ == "__main__":
    try:
        call_command('reproducer')
    except AssertionError:
        sys.exit(1)
```
To run the reproducer, execute the following command in the root directory of the project:
```
python3 reproducer.py
```
If the issue is present, the script will print the stack trace and exit with code 1. If the issue is fixed, the script will exit with code 0.