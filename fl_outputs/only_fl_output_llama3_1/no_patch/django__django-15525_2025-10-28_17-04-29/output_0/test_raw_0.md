Here is the reproducer script:

```python
import os
import sys
from django.core.management import call_command
from django.db import IntegrityError, OperationalError
from django.test.utils import CaptureStandardOutput

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

def reproduce_issue():
    try:
        with CaptureStandardOutput() as capture:
            call_command('loaddata', 'books.json', database='other')
    except (IntegrityError, OperationalError) as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    os.chdir('/path/to/your/project')  # replace with your project path
    reproduce_issue()
```

This script will change into the directory of your project and then try to load data from a file named `books.json` using the `loaddata` management command. If an error occurs, it will print the stack trace and raise an assertion error.

Please note that you should replace `/path/to/your/project` with the actual path to your Django project.