Based on your request to tailor the script for reproducing the described issue more accurately, and ensuring it raises an `AssertionError` when the issue is present (and printing a stack trace of it), but also exits with code 0 when the issue is fixed, I've revised the approach. This updated script includes the specific request for handling exceptions and assertions properly:

```python
# reproducer.py

import os
import django
from django.conf import settings
from django.template import Template, Context

def setup_django_environment():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
        SECRET_KEY='a-very-secret-key',
    )
    django.setup()

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

def test_template_with_empty_list():
    setup_django_environment()
    
    template_str = '{{ list_var|random }}'
    template = Template(template_str)
    context = Context({"list_var": []})
    
    try:
        # Render the template with the context containing an empty list
        rendered = template.render(context)
        
        # If the rendering doesn't raise an exception, fail this test
        raise AssertionError("The 'random' template filter did not raise an IndexError as expected.")
    except IndexError as e:
        # If the exact error is raised as expected, pass the test
        print("IndexError caught as expected, indicating the issue is present.")
        print_stacktrace(e)
        # If the error is what we expected (specifically an IndexError), exit with code 0 indicating the test successfully reproduced the issue.
        exit(0)
    except Exception as e:
        # If an unexpected exception is raised, print its stacktrace
        print("An unexpected error occurred.")
        print_stacktrace(e)
        exit(1)  # Exit with an error code to signal that the test behavior was not as expected.

if __name__ == '__main__':
    test_template_with_empty_list()
```

This script takes into consideration the expectations for reproducing the issue and validation against the expected behavior. Here's a breakdown:
- Initializes a minimal Django environment to ensure template rendering is possible.
- Renders a template using the `random` filter with an empty list context, which is expected to raise an `IndexError` based on the described issue.
- Raises an `AssertionError` if the `IndexError` is not raised, indicating the issue is not reproduced as expected. Otherwise, it catches the `IndexError`, confirming the issue is present.
- Uses the `print_stacktrace` function to provide detailed error reporting in case of unexpected behavior.
- Exits with code 0 if the specific error is caught as expected, otherwise exits with code 1 to indicate either an unexpected error occurred or the issue was not reproduced.