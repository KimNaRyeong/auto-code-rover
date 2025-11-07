Here is the reproducer script:

```python
import os
import django
from django.db import IntegrityError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.test.utils import CaptureStdout

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

django.setup()

class Reproducer:
    def __init__(self):
        self.app_label = 'app_authors'
        self.models_module_name = 'models'

    def run(self):
        try:
            makemigrations_command = MakemigrationsCommand()
            with CaptureStdout() as stdout_capture:
                makemigrations_command.handle(no_input=True, verbosity=0)
            if "ValueError: Found wrong number (0) of constraints for app_authors(project_data_set, state, start_date)" not in stdout_capture.stdout:
                raise AssertionError("Expected ValueError not found")
        except Exception as e:
            print_stacktrace(e)

    def print_stacktrace(self, e):
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
    repro = Reproducer()
    repro.run()
```

This script will run the makemigrations and migrate commands, capture the output, and check if the expected error message is present. If not, it raises an AssertionError with a stack trace of the exception.

Please note that you need to replace `'project'` in `os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'` with your actual Django project name.