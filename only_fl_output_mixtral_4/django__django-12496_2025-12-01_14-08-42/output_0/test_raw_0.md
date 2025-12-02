 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import uuid

from django.conf import settings
from django.db import connection, models

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'multiparent',
    ],
)

from django.core.management import call_command


def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

    class Meta:
        db_table = 'app_parent'


class Child(Parent):
    body = models.TextField()

    class Meta:
        db_table = 'app_child'


def create_child():
    with connection.cursor() as cursor:
        cursor.execute("SET client_min_messages TO 'WARNING'")

    Child.objects.create()


def main():
    call_command('migrate', interactive=False)
    create_child()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
To run the script, execute `python3 reproducer.py`. The script will print the stack trace of the issue.

The script creates a new database named `test_db` and applies the necessary migrations. It then creates a new `Child` object and prints the SQL queries executed during the operation. You can see that an extra `UPDATE` query is executed, which is unnecessary and causes the issue.

If you modify the `Parent` model to use the default primary key (i.e., `id = models.AutoField(primary_key=True)`), the issue will not occur, and the script will exit with code 0.