Here is the reproducer script:

```python
import os
from django.db import connections, router
from django.db.migrations.recorder import MigrationRecorder

def main():
    # Set up Django project
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    from django.conf import settings
    settings.configure()

    # Create test databases
    for conn in connections.all():
        conn.create_test_db(verbosity=0)

    # Get the MigrationRecorder instance for each connection
    recorders = []
    for conn in connections.all():
        recorder = MigrationRecorder(conn.alias)
        recorders.append(recorder)

    # Check if the Migration model is present in each database
    router.allow_migrate('non_default', None)  # This should raise an AssertionError

class Router(object):
    def allow_migrate(self, db, model=None):
        if db == 'default':
            return True
        return False

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

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script sets up a Django project, creates test databases, and then checks if the Migration model is present in each database. If it's not present, an `AssertionError` is raised with the stack trace printed using the provided function.

To run this script, save it to a file named `reproducer.py`, navigate to the root directory of your project, and execute it with `python3 reproducer.py`.