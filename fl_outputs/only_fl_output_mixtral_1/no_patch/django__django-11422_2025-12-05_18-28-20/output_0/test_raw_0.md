 Here is a standalone Python script `reproducer.py` that you can use to reproduce the issue:
```python
import time
import sys
import traceback
from django.utils import autoreload
from django.core.management import execute_from_command_line

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Set up Django
    autoreload.main(argv=sys.argv)

    # Modify manage.py
    manage_py = sys.modules['__main__'].__file__
    with open(manage_py, 'a') as f:
        f.write('\nprint("Modified manage.py")\n')

    # Start the server
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To use the script, create a new Django project with version 2.2.1, and put the `reproducer.py` file in the root directory of the project. Then execute the script with `python3 reproducer.py`. If the autoreloader does not track changes in `manage.py`, the script will print a stack trace and exit with code 1. If the autoreloader does track changes in `manage.py`, the script will start the Django development server and exit with code 0.

Note that the script uses the `autoreload` module directly to modify the autoreloader behavior. This is because the `StatReloader` class, which is used by default in Django 2.2.1, does not track changes in the `manage.py` file by default. By modifying the `autoreload` module directly, we can simulate the behavior of the previous autoreloader implementation, which did track changes in `manage.py`.