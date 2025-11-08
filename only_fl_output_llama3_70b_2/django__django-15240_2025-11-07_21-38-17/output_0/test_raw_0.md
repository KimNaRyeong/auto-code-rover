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

def main():
    # Create a new Django project
    os.system("django-admin startproject myproject")
    os.chdir("myproject")

    # Create an app with some migrations
    os.system("python manage.py startapp myapp")
    os.system("python manage.py makemigrations myapp")
    os.system("python manage.py migrate")

    # Squash and delete replaced migrations
    os.system("python manage.py squashmigrations myapp 0003")
    os.remove("myapp/migrations/0001_initial.py")
    os.remove("myapp/migrations/0002_blah.py")
    os.remove("myapp/migrations/0003_blah.py")

    # Create a new migration with the same name as one that was applied in the past
    os.system("python manage.py makemigrations myapp")

    # Try to apply the new migration, which should fail due to the issue
    try:
        execute_from_command_line(["manage.py", "migrate"])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("New migration did not run due to deleted migrations in django_migrations table")

if __name__ == "__main__":
    main()
```
This script creates a new Django project, app, and some migrations. It then squashes and deletes replaced migrations, creating a situation where the `django_migrations` table contains references to non-existent migrations. Finally, it tries to apply a new migration with the same name as one that was applied in the past, which should fail due to the issue.

When run with `python3 reproducer.py`, this script will raise an `AssertionError` if the issue is present and print a stack trace of the error. If the issue is fixed, it will exit with code 0.