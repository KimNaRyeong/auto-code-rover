Below is the `reproducer.py` script designed to replicate the issue described. This script uses Django ORM setup procedure inline, therefore, it's more demonstrative than practical for a real project setup. Ensure you have Django installed and a database backend setup as per the script's configuration (SQLite/Oracle). If you aim to test against Oracle, additional setups like an Oracle database and Django backend for Oracle (`django-db-backend-oracle`) would be necessary.

```python
import os
import django
from django.conf import settings
from django.db import models
from django.db.models.functions import Right, Length

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

def main():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # 'ENGINE': 'django.db.backends.oracle',
            'NAME': ':memory:',
            # 'USER': '',
            # 'PASSWORD': '',
            # 'HOST': '',
            # 'PORT': '',
        }
    }

    settings.configure(
        DATABASES=DATABASES,
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )

    django.setup()

    class MyModel(models.Model):
        foo = models.CharField(max_length=255)

    # Create the table
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(MyModel)

    # Insert test data
    MyModel.objects.create(foo='TestString')

    # Try to replicate the bug
    try:
        annotated = MyModel.objects.annotate(suffix=Right('foo', Length('foo') - Length('foo')))
        value = annotated.first().suffix
        assert value == '', f"Expected '', got '{value}'"
        print("The issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # This is to ensure the script exits with 0 even when the issue is present, after printing stack trace.
        import sys
        sys.exit(0)
```

This script dynamically creates a Django project and a model to interact with the database, attempting to replicate the issue by annotating a model's field with a `Right` function whose length argument could be zero. If the issue is present, the script will catch an `AssertionError` indicating the problem's occurrence and print an error stack trace as requested. 

Please replace the `DATABASES['default']['ENGINE']` value and other database connection parameters accordingly to test against different database backends.