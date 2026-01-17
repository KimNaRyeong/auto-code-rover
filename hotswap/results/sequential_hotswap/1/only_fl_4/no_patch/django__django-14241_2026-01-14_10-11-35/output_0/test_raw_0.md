```python
import os
import django
from django.conf import settings
from django.db import models

# Minimal Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    BASE_DIR=BASE_DIR,
)


class Celebrity(models.Model):
    name = models.CharField(max_length=100)


class ReservedName(models.Model):
    name = models.CharField(max_length=100)


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


def check_issue():
    try:
        django.setup()
        from django.db import connection
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Celebrity)
            schema_editor.create_model(ReservedName)
        qs1 = Celebrity.objects.all()
        qs2 = ReservedName.objects.all()
        result = qs1.union(qs2).values_list('name').first()
        assert result is not None, "Union query did not return a result as expected"

    except AssertionError as e:
        # This captures the expected assertion and any related information when the issue is present
        print_stacktrace(e)
        raise

    except Exception as e:
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    check_issue()
```