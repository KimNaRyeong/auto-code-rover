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
    os.makedirs("myapp/migrations", exist_ok=True)
    with open("myapp/migrations/__init__.py", "w") as f:
        pass

    # Create initial migration
    execute_from_command_line(["manage.py", "makemigrations", "myapp"])
    assert os.path.exists("myapp/migrations/0001_initial.py")

    # Apply the initial migration
    execute_from_command_line(["manage.py", "migrate"])

    # Squash and delete replaced migrations
    with open("myapp/migrations/0001_squashed_0003_blah.py", "w") as f:
        pass
    os.remove("myapp/migrations/0001_initial.py")
    os.remove("myapp/migrations/0002_blah.py")
    os.remove("myapp/migrations/0003_blah.py")

    # Create a new migration with the same name as one that was applied in the past
    execute_from_command_line(["manage.py", "makemigrations", "myapp"])
    assert os.path.exists("myapp/migrations/0002_blah.py")

    # Try to apply the new migration (should fail because Django thinks it's already been applied)
    try:
        execute_from_command_line(["manage.py", "migrate"])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("New migration did not run due to duplicate name in django_migrations table")

if __name__ == "__main__":
    main()
```
This script creates a new Django project, app, and migrations, applies the initial migration, squashes and deletes replaced migrations, creates a new migration with the same name as one that was applied in the past, and tries to apply it. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.

To run the script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.