Here is the `reproducer.py` script to reproduce the issue:
```
import os
import sys
from django.core.management import execute_from_command_line
from django.db.migrations.recorder import MigrationRecorder

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

def create_migration(app_name, migration_name):
    management_dir = os.path.join(os.getcwd(), 'manage.py')
    execute_from_command_line(['python', management_dir, 'makemigrations', app_name, '--empty', migration_name])

def squash_migrations(app_name):
    management_dir = os.path.join(os.getcwd(), 'manage.py')
    execute_from_command_line(['python', management_dir, 'squashmigrations', app_name])

def delete_migration(migration_file):
    os.remove(migration_file)

def main():
    app_name = 'my_app'
    initial_migration = '0001_initial.py'
    blah_migration = '0002_blah.py'
    squashed_migration = '0001_initial_squashed_0003_blah.py'

    # Create initial migration
    create_migration(app_name, initial_migration)

    # Apply initial migration
    execute_from_command_line(['python', 'manage.py', 'migrate'])

    # Create blah migration
    create_migration(app_name, blah_migration)

    # Apply blah migration
    execute_from_command_line(['python', 'manage.py', 'migrate'])

    # Squash migrations
    squash_migrations(app_name)

    # Delete replaced migrations
    delete_migration(os.path.join(app_name, 'migrations', initial_migration))
    delete_migration(os.path.join(app_name, 'migrations', blah_migration))

    # Create new migration with same name as old one
    create_migration(app_name, initial_migration)

    try:
        # Apply new migration (should fail because django_migrations table thinks it's already been applied)
        execute_from_command_line(['python', 'manage.py', 'migrate'])
        assert False, "Migration should not have been applied"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
This script creates a Django project with an app `my_app`, applies some migrations, squashes them, deletes the replaced migrations, and then tries to apply a new migration with the same name as one of the old ones. If the issue is present, it should raise an `AssertionError` when trying to apply the new migration.

To use this script, create a new Django project with an app `my_app`, and put this script in the root directory of the project. Then, run `python3 reproducer.py`.