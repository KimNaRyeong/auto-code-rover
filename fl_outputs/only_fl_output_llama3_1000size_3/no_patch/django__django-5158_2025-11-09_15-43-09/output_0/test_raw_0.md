Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line

def main():
    try:
        os.chdir('/path/to/non-existent/project')
        execute_from_command_line(['django-admin.py', 'not-a-real-command', 'test'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == '__main__':
    main()
```

This script attempts to change the current directory to a non-existent project, then tries to execute the `django-admin.py` command with an unknown subcommand. If the issue is present (i.e., Django raises an `ImproperlyConfigured` exception), it prints the stack trace and raises an `AssertionError`.