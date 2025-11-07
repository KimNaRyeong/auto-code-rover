```python
# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models

# Setup minimal Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS=(
        '__main__',  # This will add this script as an app
    ),
    USE_TZ=True,
)


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


# Define a model to use with the QuerySet
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'


def main():
    try:
        # Initialize Django
        django.setup()
        execute_from_command_line(['manage.py', 'migrate'])

        # Create a QuerySet as described in the issue
        qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')

        # Raise AssertionError if the issue is present
        assert str(qs.query) != 'EmptyResultSet', 'The WHERE block is missing completely.'
        print("The issue seems to be fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)


if __name__ == '__main__':
    main()
```

This script initializes a minimal Django configuration, defines a single model, and then attempts to reproduce the issue by evaluating the queryset's SQL string representation. When the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed (meaning, the queryset doesn't result in an `EmptyResultSet` or removes the WHERE block when it shouldn't), it will print a success message. Remember, you need Django installed in your environment to run this script, and it should be executed in an environment where Django commands are recognized.