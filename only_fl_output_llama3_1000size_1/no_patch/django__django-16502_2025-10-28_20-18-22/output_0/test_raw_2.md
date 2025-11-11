Here is the reproducer script:

```python
import os
import subprocess
import sys
from django.core.management import execute_from_command_line

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
        os.system('django-admin startproject django-test')
        os.chdir('django-test')
        process = subprocess.Popen(['./manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if b'<!DOCTYPE html>' in output and not error.decode().startswith('Broken pipe'):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    reproduce_issue()
```

This script will create a new Django project, start the development server, and check if the output contains the HTML tag and there is no error message starting with 'Broken pipe'. If these conditions are met, it will raise an `AssertionError`.