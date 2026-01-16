```python
import os
import sys
from django.db import models
from django.db.models.functions import ExtractYear
from django.core.management import execute_from_command_line
from django.conf import settings


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


class MyModel(models.Model):
    duration = models.DurationField()


def main():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            __name__,
        ],
        USE_TZ=True,
    )
    execute_from_command_line(['manage.py', 'migrate'])

    try:
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        # If the above line doesn't raise an error, we assume the issue is fixed.
        print("The issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is still present.") from e


if __name__ == '__main__':
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer.settings")
        main()
    except AssertionError as err:
        print(f"Assertion failed: {err}")
        sys.exit(0)
```

Ensure you have Django installed in your environment (`pip install django`) and run this script with Python 3. The script sets up a minimal Django environment, defines a model with a `DurationField`, and tries to perform an operation that is known to raise an exception due to the misuse of `ExtractYear` with `DurationField`s. If the issue described is present, it will print the stack trace using the provided `print_stacktrace` function and exit with code 0, signaling that the reproduction was successful and the issue still exists. Conversely, if the operation unexpectedly succeeds, the script will assume the issue has been fixed and print a corresponding message.