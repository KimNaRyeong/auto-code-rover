Here is the reproducer script:

```python
import os
import django
from django.db import connections, router
from django.db.migrations.recorder import MigrationRecorder
from django.test.runner import DiscoverRunner

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()

    router_instance = Router()
    connections.create_test_db('test_default', keepdb=True, create_all=False, using='default')
    connections.create_test_db('test_non_default', keepdb=True, create_all=False, using='non_default')

    recorder = MigrationRecorder(connections['default'])
    try:
        recorder.record_applied('app_name', '0001_initial')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script sets up a test database for the default connection and another test database for a non-default connection. It then tries to record an applied migration on the default connection, which should fail due to the router not allowing migrations on the non-default connection. The script prints the stack trace of the exception and raises it again.

To run this script, save it in a file named `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.