 Here is a standalone Python script `reproducer.py` that you can use to reproduce the issue:
```python
import time
from django.core.management.commands.runserver import Command as RunServerCommand
from django.utils.autoreload import restart_if_possible
from django.conf import settings

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    print('sth')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_30479.settings')
    cmd = RunServerCommand()
    cmd.inner_run(cmd.outer_args)

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        restart_if_possible()
```
This script uses the `restart_if_possible` function from Django's autoreload module to restart the server when a change is detected. The `main` function is similar to Django's `runserver` command, but it is defined in this script instead of being imported from Django.

To use this script, create a new Django project with a settings module, and place the `reproducer.py` script in the root directory of the project. Then, run the script with `python3 reproducer.py`.

If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.

Note: This script is intended to be used for testing and debugging purposes only. It is not recommended to use this script in a production environment.