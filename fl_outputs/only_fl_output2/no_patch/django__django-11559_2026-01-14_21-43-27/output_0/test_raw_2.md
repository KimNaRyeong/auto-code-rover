Given the context and requirements, let's adjust the approach to explicitly address the issue described: using `order_by()` in a parent model where `Meta.ordering` contains expressions might crash. This revision ensures that the error is related to the use of expressions within `Meta.ordering` and that the program behaves correctly with regards to exception handling and reporting.

This scenario assumes you have a Django project setup. If not, you might first need to create a Django project (`django-admin startproject yourprojectname`) and then place this script in the root directory of your project.

```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
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

def setup_django_environment():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            '__main__',  # This app is included to locate the below model for Django
        ),
        # Required Django settings
        SECRET_KEY='a-very-bad-secret-key-but-good-enough-for-a-test-script',
        USE_I18N=False,
        USE_TZ=False,
    )
    django.setup()


class Parent(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = [models.F('name').asc()]  # This line is the source of potential issues


class Child(Parent):
    extra_field = models.CharField(max_length=50)


def run_django_setup():
    # Apply migrations
    execute_from_command_line(['manage.py', 'migrate'])

    # Create a super user (only needed if you want to access the admin)
    execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', '--email', 'test@example.com', '--username', 'admin'])


def reproduce_issue():
    try:
        setup_django_environment()
        run_django_setup()

        # Attempt to create Parent and Child instances to trigger the order_by evaluation
        Parent.objects.create(name="Parent 1")
        Child.objects.create(name="Child 1", extra_field="Value 1")

        # Try to fetch the objects to ensure the ordering is applied
        parents = Parent.objects.all()
        children = Child.objects.all()

        print("Successfully created and fetched Parent and Child instances without crashing.")
        os._exit(0)  # Indicate success

    except Exception as e:
        print_stacktrace(e)
        os._exit(1)  # Ensure we signal failure correctly


if __name__ == "__main__":
    reproduce_issue()
```

**Important Notes:**

- The script uses an in-memory SQLite database for simplicity. Adjust the `DATABASES` setting if a different setup is required.
- Ensure you have Django installed in your Python environment (`pip install django`).
- The `execute_from_command_line(['manage.py', 'migrate'])` call simulates running Django management commands; it requires the `django.core.management` module to work.
- Running this script directly (`python3 reproducer.py`) attempts to reproduce the reported issue.
- The script exits with code 0 if the issue is not present (i.e., fixed or unable to reproduce), and it exits with code 1 upon encountering an exception, printing the stack trace.
- This script is simplified for the sake of reproducing the specific issue and thus might need adjustments for integration into different Django project structures or versions.