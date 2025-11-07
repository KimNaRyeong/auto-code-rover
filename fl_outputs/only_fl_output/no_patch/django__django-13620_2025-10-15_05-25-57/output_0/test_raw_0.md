Below is the `reproducer.py` file that meets your criteria. This script will attempt to execute the command with list arguments. If the issue is present, it will catch the `CommandError` raise by Django when it incorrectly processes the list argument for `--foo`, then it will print the stack trace. If the issue does not occur (meaning it is fixed), the script will simply exit with code 0.

```python
import sys
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core import management
from django.apps import apps
import django

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Command(BaseCommand):
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--foo', nargs='+', type=int)

    def handle(self, *args, **options):
        pass

if __name__ == "__main__":
    # Minimal setup for Django
    apps.populate(installed_apps=['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.messages'])
    management.setup_environ(django.conf.settings)
    django.setup()
    
    try:
        # Attempt to invoke the command with list arguments
        call_command('reproducer', foo=[1, 2, 3])
        # If no error, assume issue is resolved
        print("Issue is resolved")
    except CommandError as e:
        # If the specific issue occurs, print stack trace
        print_stacktrace(e)
        assert "argument --foo: invalid int value: '[1, 2, 3]'" in str(e)
```

To use this script:
1. Ensure Django is installed in your environment (`pip install django`).
2. Place this script in the root directory of your Django project.
3. Execute the script using `python3 reproducer.py`.

**Note:** Understand that this script requires a minimal Django setup to run. It has been simplified by populating Django apps and setting up the environment within the script itself. Depending on your project's configuration, you may need to adjust the `apps.populate` line to include apps relevant to your project or modify the setup to match your specific Django settings structure.