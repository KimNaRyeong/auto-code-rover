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
    os.system(f"python manage.py makemigrations {app_name} --empty --name {migration_name}")

def squash_migrations(app_name):
    os.system(f"python manage.py squashmigrations {app_name} 0001")

def delete_migration(migration_file):
    os.remove(migration_file)

def main():
    app_name = "my_app"
    migration_dir = f"{app_name}/migrations"

    # Create initial migrations
    create_migration(app_name, "initial")
    execute_from_command_line(["manage.py", "migrate"])

    # Create additional migrations
    create_migration(app_name, "blah1")
    create_migration(app_name, "blah2")

    # Squash and delete replaced migrations
    squash_migrations(app_name)
    delete_migration(f"{migration_dir}/0002_blah1.py")
    delete_migration(f"{migration_dir}/0003_blah2.py")

    # Create a new migration with the same name as an old one
    create_migration(app_name, "initial_squashed_0003_blah2")

    # Try to apply the new migration (should fail)
    try:
        execute_from_command_line(["manage.py", "migrate"])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Migration should not have been applied"

    # Check if the django_migrations table still contains the old migration
    recorder = MigrationRecorder(None)
    applied_migrations = recorder.applied_migrations()
    assert ("my_app", "0002_blah1") in applied_migrations, "Old migration should still be present in django_migrations table"
    print("Issue reproduced successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
```
This script creates a Django project with an app `my_app`, creates some migrations, squashes and deletes them, and then tries to apply a new migration with the same name as an old one. If the issue is present, it should raise an `AssertionError` when trying to apply the new migration, and print a stack trace of the error. If the issue is fixed, the script should exit with code 0.

Please note that this script assumes you have Django installed and configured properly in your project. Also, make sure to run this script from the root directory of your project.