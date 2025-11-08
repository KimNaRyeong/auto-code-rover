I apologize for the previous mistake. Here is a new `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    },
    INSTALLED_APPS=['app'],
)

class Parent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()

class Child(Parent):
    body = models.TextField()

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

try:
    setup_test_environment()
    from django.core.management import call_command
    call_command('makemigrations', 'app')
    call_command('migrate')

    child = Child.objects.create()

    # Check if the issue is present
    with open(os.devnull, "w") as f:
        sys.stdout = f
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM pg_stat_statements WHERE query LIKE '%UPDATE \"app_parent\" SET \"title\" = \'\'%';")
            result = cursor.fetchone()
            if result:
                raise AssertionError("Issue is present: Extra update query is executed")
        finally:
            sys.stdout = sys.__stdout__

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django project with a custom primary key on the `Parent` model, creates a `Child` object, and checks if an extra update query is executed. If the issue is present, it raises an `AssertionError`.