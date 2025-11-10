Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

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
    settings.configure()
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, and then tries to run the development server. If an exception is raised, it prints the stack trace and exits with code 1.

Please replace `'your_project.settings'` with your actual project settings module name.