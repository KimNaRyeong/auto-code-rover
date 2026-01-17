import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models.functions import Right, Length

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

def main():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Adjust as necessary for Oracle or other DBs
            'NAME': ':memory:',
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

    try:
        # Attempt to replicate the reported issue
        annotated = MyModel.objects.annotate(suffix=Right('foo', Length('foo') - Length('foo')))
        result = annotated.first().suffix

        assert result == '', f"Expected '', got '{result}'"
        
        # Exiting with 0 if no issue is detected
        sys.exit(0)
        
    except AssertionError as e:
        print_stacktrace(e)
        # Exiting with a non-zero code to indicate an issue
        sys.exit(1)

if __name__ == "__main__":
    main()
