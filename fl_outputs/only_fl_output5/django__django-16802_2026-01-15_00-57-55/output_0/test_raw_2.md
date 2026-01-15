To accurately reproduce the reported issue and incorporate the request for stack trace printing in case of failure, you can utilize the following script. This script specifically targets the behavior of the `random` template filter in Django when used with an empty list. The expected behavior is that it should not throw an `IndexError` and should consistently handle an empty list like the `first` and `last` filters do.

```python
# reproducer.py
import os
import sys
from django.conf import settings
from django.template import Template, Context

MINIMAL_SETTINGS = {
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ],
    'SECRET_KEY': 'abc123',
}

def setup_django_environment():
    settings.configure(**MINIMAL_SETTINGS)
    try:
        # Setup Django
        import django
        django.setup()
    except AttributeError:
        # Depending on the Django version, an AttributeError might occur if setup is called more than once.
        pass

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

def reproduce_issue():
    setup_django_environment()
    template_code = '{{ list_var|random }}'
    template = Template(template_code)
    context = Context({"list_var": []})
    try:
        # This is where the random filter is applied to an empty list
        rendered = template.render(context)
        # If an IndexError did not occur, it means the issue is potentially fixed, or the environment is not replicating the issue.
        print("Test passed: No exception was raised by the 'random' filter with an empty list.")
        sys.exit(0)
    except Exception as e:
        if isinstance(e, IndexError):
            print("Issue reproduced: 'random' filter raised an IndexError on an empty list.", file=sys.stderr)
            print_stacktrace(e)
            # Exiting with non-zero to indicate the presence of the Issue
            sys.exit(1)
        else:
            print("An unexpected error occurred:", file=sys.stderr)
            print_stacktrace(e)
            sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

Instructions for using the script:

1. **Place the script** in the root of a Django project.
2. **Execute the script** using Python 3. Ensure Django is installed in your environment.
3. The script will **automatically configure** a minimal Django environment required to reproduce the issue.
4. It executes a template rendering with the `random` filter applied to an empty list to simulate the reported error condition.
5. If the issue is encountered (i.e., an `IndexError` is raised), it prints the stack trace using the provided function.
6. It exits with a status code indicating whether the issue has been reproduced (`1`) or if no error occurred (`0`).
