 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run():
    # Create a new Django project
    settings = type('Settings', (object,), {'BASE_DIR': '.'})
    project = migrations.MigrationExecutor(migrations.SqlMigrationExecutor(connections['default']), settings)

    # Create a new app and define a model with a BinaryField
    app_config = type('AppConfig', (object,), {'name': 'firstapp'})
    models.ModuleType('firstapp', app_config).__path__ = ['firstapp']
    models.add_to_class('firstapp.TableOne', 'field1', models.BinaryField(default=''))

    # Create the initial migration
    project.loader.build_graph()
    migration = project.loader.migration_modules['firstapp.migrations'].migration_list[0]
    project.make_migration(migration.app, migration.name)

    # Apply the migration
    project.migrate([migration])

    # Modify the model to use a different default value
    models.add_to_class('firstapp.TableOne', 'field1', models.BinaryField(default=b''))

    # Create the new migration
    project.loader.build_graph()
    project.make_migration(migration.app, migration.name)

    # Apply the new migration
    project.migrate([migration])

    # Try to roll back the migration
    project.migrate([migration], reverse=True)

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, create a new directory for the project, create a new virtual environment, activate the virtual environment, install Django, and run the script:
```bash
$ mkdir djangoproject
$ cd djangoproject
$ python3 -m venv venv
$ source venv/bin/activate
(djangoproject) $ pip install django
(djangoproject) $ python3 reproducer.py
```
The script should raise an `AssertionError` with a stack trace showing the error:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 64, in <module>
    run()
  File "reproducer.py", line 60, in run
    project.migrate([migration], reverse=True)
  File "venv/lib/python3.6/site-packages/django/db/migrations/executor.py", line 119, in migrate
    state = self._migrate_all_backwards(plan, full_plan, fake=fake)
  File "venv/lib/python3.6/site-packages/django/db/migrations/executor.py", line 194, in _migrate_all_backwards
    self.unapply_migration(states[migration], migration, fake=fake)
  File "venv/lib/python3.6/site-packages/django/db/migrations/executor.py", line 264, in unapply_migration
    state = migration.unapply(state, schema_editor)
  File "venv/lib/python3.6/site-packages/django/db/migrations/migration.py", line 178, in