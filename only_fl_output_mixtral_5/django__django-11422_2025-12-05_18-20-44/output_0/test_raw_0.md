 Here is a standalone Python script `reproducer.py` that you can use to reproduce the issue:
```python
import time
from django.core.management.commands.runserver import Command as RunServerCommand
from django.utils.autoreload import restart_if_possible, get_restart_files
from django.core.management import management

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
    management.execute_from_command_line(cmd._args)

if __name__ == '__main__':
    try:
        while True:
            main()
            restart_files = get_restart_files()
            if not restart_files:
                print('No restart files found. Sleeping for 1 second.')
                time.sleep(1)
            else:
                print('Restart files found. Restarting...')
                restart_if_possible()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
