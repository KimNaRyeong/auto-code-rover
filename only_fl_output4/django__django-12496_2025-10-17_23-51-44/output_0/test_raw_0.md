```python
import uuid
import os
import django
from django.conf import settings
from django.db import models, connection

# Django setup
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'yourdbname',
            'USER': 'yourdbuser',
            'PASSWORD': 'yourdbpassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


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
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Parent)
        schema_editor.create_model(Child)
    
    try:
        # Capturing the executed queries
        with connection.cursor() as cursor:
            cursor.execute('BEGIN;')
            cursor.execute('SET session_replication_role = replica;')  # Disable triggers to keep track of raw queries
            try:
                Child.objects.create()
                executed_queries = connection.queries
            finally:
                cursor.execute('ROLLBACK;')
        
        # Looking for unexpected 'UPDATE' query
        update_queries = [query for query in executed_queries if query['sql'].startswith('UPDATE')]
        assert len(update_queries) == 0, "Unexpected 'UPDATE' query found"
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```

Please replace `'yourdbname'`, `'yourdbuser'`, and `'yourdbpassword'` with your actual database credentials. This script sets up a minimal Django environment, defines two models to reproduce the issue specified, and checks for the unexpected 'UPDATE' query. If the issue is found (`AssertionError` is raised), it prints a stack trace showing where the issue occurs. If your environment is configured correctly, and the Django version you're using hasn't fixed this issue yet, the script will exhibit the behavior described and exit accordingly.