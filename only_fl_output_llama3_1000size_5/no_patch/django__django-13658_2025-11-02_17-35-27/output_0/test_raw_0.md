Here is the reproducer script:

```python
import sys
from django.core.management import ManagementUtility

def main():
    utility = ManagementUtility(argv=['django-admin.py', 'test'])
    parser = utility.create_parser()
    try:
        parser.parse_args(['--help'])
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            print("Test failed", file=sys.stderr)
        else:
            print("Test passed")
```

This script creates a `ManagementUtility` instance with the program name set to `'django-admin.py'`, then attempts to parse the command-line arguments. If an `AssertionError` is raised, it prints the stack trace and re-raises the exception.