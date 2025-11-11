Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line

def main():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
    try:
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == '__main__':
    main()
```

Replace `'your_project'` with the name of your Django project. This script sets up a Django environment and runs the development server using `manage.py runserver`. If an exception occurs during this process, it prints the stack trace and raises an `AssertionError`.

You can execute this script by running `python3 reproducer.py` in the root directory of your project.