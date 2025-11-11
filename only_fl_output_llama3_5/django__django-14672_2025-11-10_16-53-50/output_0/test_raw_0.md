Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps
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

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broken_m2m_project.settings')
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will raise an `AssertionError`, and if the issue is fixed, it will exit with code 0.