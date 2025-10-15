```python
# reproducer.py
import uuid
import os
import django
from django.conf import settings
from django.db import models, connection
from django.core.management import call_command


def setup():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )
    django.setup()


def create_tables():
    call_command('makemigrations', '--noinput', '--dry-run')
    call_command('migrate', '--noinput')


class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

    class Meta:
        app_label = '__main__'


class Child(Parent):
    body = models.TextField()

    class Meta:
        app_label = '__main__'


def verify_issue():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='parent';")
        assert cursor.fetchone()[0] == 1, "Parent table does not exist."

    # Attempt to create a Child instance—which in turn should create a Parent instance
    child_instance = Child.objects.create()

    # Verifying if only INSERT statements are used for both Parent and Child tables
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM sqlite_sequence WHERE name='__main___parent';")
        parent_insert_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM sqlite_sequence WHERE name='__main___child';")
        child_insert_count = cursor.fetchone()[0]
        if parent_insert_count != 1 or child_insert_count != 1:
            raise AssertionError("Unexpected number of INSERT operations for Parent or Child.")

        # Check for UPDATE operations that should not exist
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='trigger';")
        triggers = cursor.fetchall()
        if any("UPDATE" in trigger[0] for trigger in triggers):
            raise AssertionError("Unexpected UPDATE operation found.")

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


if __name__ == '__main__':
    setup()
    create_tables()

    try:
        verify_issue()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)  # Exit with status code 1 indicating failure
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        raise SystemExit(1)  # Exit with status code 1 indicating failure
    else:
        SystemExit(0)  # Exit with status code 0 indicating success
```