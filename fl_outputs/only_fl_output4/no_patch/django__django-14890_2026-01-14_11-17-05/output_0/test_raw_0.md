```python
import os
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# Minimal Django settings required for running the script
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)


class MyModel(models.Model):
    name = models.CharField(max_length=100)

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


def main():
    django.setup()
    call_command('migrate', verbosity=0)

    # Creating test data
    for name in ['a', 'b', 'c']:
        MyModel.objects.create(name=name)

    group1 = MyModel.objects.filter(name='a')
    group2 = MyModel.objects.filter(name='b')
    group3 = MyModel.objects.filter(name='c')
    combined_group = group1.union(group2)

    # Applying & and | operators after union
    try:
        group_and = combined_group & group1
        group_or = combined_group | group3

        # Checking if the SQL queries are different as expected
        combined_sql = str(combined_group.query)
        group_and_sql = str(group_and.query)
        group_or_sql = str(group_or.query)

        assert combined_sql != group_and_sql, "Combined and group1 SQL should NOT be the same"
        assert combined_sql != group_or_sql, "Combined and group3 SQL should NOT be the same"

    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)

    # This block is only reached if no AssertionError has occurred
    print("Issue is fixed, exiting with code 0")
    os._exit(0)


if __name__ == '__main__':
    main()
```