Here is the reproducer script:

```python
import os
from django.core.management import execute_from_command_line
from django.conf import settings

def main():
    # Set up Django environment
    settings.configure(
        INSTALLED_APPS=['your_project'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }
    )
    try:
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

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
    main()
```

Replace `'your_project'` with the name of your Django project. This script sets up a Django environment and runs the development server using `manage.py runserver`. If an exception occurs during this process, it prints the stack trace and exits with code 1.

To reproduce the issue, save this script to a file named `reproducer.py`, replace `'your_project'` with your project name, and then execute it by running `python3 reproducer.py`.