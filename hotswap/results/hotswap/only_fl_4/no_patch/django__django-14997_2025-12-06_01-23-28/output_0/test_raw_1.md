 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management.base import BaseCommand
from django.db import connection, migrations
from django.db.backends.utils import DatabaseWrapper
from django.db.models import F, SlugField, CharField
from django.utils.timezone import now

class MockDatabaseWrapper(DatabaseWrapper):
    def _remake_table(self, model, alter_field=None):
        sql = "CREATE TABLE myapp_tag (" \
              "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
              "name TEXT NOT NULL," \
              "value TEXT NOT NULL," \
              "UNIQUE (name, value)" \
              ");"
        with connection.cursor() as cursor:
            cursor.execute(sql)

        sql = "ALTER TABLE myapp_tag RENAME TO myapp_tag__old;"
        with connection.cursor() as cursor:
            cursor.execute(sql)

        sql = "CREATE TABLE myapp_tag (" \
              "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
              "name TEXT NOT NULL," \
              "value TEXT NOT NULL," \
              "UNIQUE (name, value)" \
              ");"
        with connection.cursor() as cursor:
            cursor.execute(sql)

        sql = "INSERT INTO myapp_tag (name, value) SELECT name, value FROM myapp_tag__old;"
        with connection.cursor() as cursor:
            cursor.execute(sql)

        sql = "DROP TABLE myapp_tag__old;"
        with connection.cursor() as cursor:
            cursor.execute(sql)

class MockMigration(migrations.Migration):
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(help_text='The tag key.')),
                ('value', models.CharField(help_text='The tag value.', max_length=200)),
            ],
            options={
                'ordering': ['name', 'value'],
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(F('name'), F('value'), name='unique_name_value'),
        ),
    ]

class MockMigration2(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]
    operations = [
        migrations.AlterField(
            model_name='tag',
            name='value',
            field=models.CharField(help_text='The tag value.', max_length=150),
        ),
    ]

class Command(BaseCommand):
    help = 'Reproduce the SQLite error'

    def handle(self, *args, **options):
        try:
            connection.features.databases['sqlite3'] = MockDatabaseWrapper
            migrations.migrations.migrations.add_to_registry(MockMigration)
            migrations.migrations.migrations.add_to_registry(MockMigration2)
            migrations.apply_final_migration()
        except Exception as e:
            print_stacktrace(e)
            assert False, 'SQLite error should be raised here'
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. The script should print the stack trace and raise an `AssertionError` when the issue is present. When the issue is fixed, the script should exit with code 0.

The script uses a mock `DatabaseWrapper` to reproduce the issue. The `_remake_table` method in the mock wrapper creates a table with a unique constraint, renames the table, creates a new table with the same schema, and inserts the data from the old table into the new table. This process triggers the SQLite error when the `max_length` of the `value` field is changed in the second migration.

The script also uses mock migrations to simulate the migrations in the issue description. The first migration creates a `Tag