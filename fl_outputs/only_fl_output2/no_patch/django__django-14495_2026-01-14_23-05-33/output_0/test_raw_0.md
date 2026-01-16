To create a script named `reproducer.py` that automates the reproduction of the described issue, we need to simulate Django's migration commands programmatically. This involves creating a Django environment, setting up an application with migrations, and then trying to migrate to a specific state that causes the issue. Since reproducing the exact setup (including the squashed migration) and the commands might be complex through a script, this example takes an abstracted approach. It will focus on the essential parts required to trigger the `KeyError` described when attempting to migrate to a specific point using Django's internal APIs. For this script to work, ensure your Django project is set up correctly, and adjust paths and names as necessary for your project structure.

```python
import os
import sys
import django
from django.core.management import call_command
from django.conf import settings

# Function to print stack trace
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

# Configuration (Adjust as necessary)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        'testproj.apps.TestprojConfig',  # Adjust this to your app configuration
    ],
    MIGRATION_MODULES={'testproj': 'testproj.migrations'},  # Point this to your app's migration folder
)

django.setup()

try:
    # Simulate the migration command to a specific state that is known to cause the issue
    call_command('migrate', 'testproj', '0001_initial')
    # If the command was successful, the issue is considered fixed, exiting with code 0
    print("Issue fixed.")
    sys.exit(0)
except Exception as e:
    # If an exception is caught, it might be the described issue. Verify by checking the exception type and content.
    if isinstance(e, KeyError) and "'0001_initial'" in str(e):
        print_stacktrace(e)
        assert False, "Issue reproduced: KeyError encountered when migrating backward to a replaced migration."
    else:
        # If the exception does not match the specific issue profile, re-raise it for clarity.
        raise e from None
```

This script is simplified to demonstrate the concept of reproducing the mentioned issue. For real-world scenarios, especially when dealing with Django's ORM and migration system, consider the complexities of your specific application structure, migration files, and settings. This script requires that your Django project is set up with an `INSTALLED_APPS` setting included for your app (here referred to as `'testproj.apps.TestprojConfig'`), and you must have the migrations already created as described in the issue. Adjust the script to fit your actual project path and app configuration.