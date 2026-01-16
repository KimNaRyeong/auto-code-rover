```python
import os
import django
from django.conf import settings
from django.db import models

# Minimal Django project settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script will be the main app
    ]
)

django.setup()

class MyModel(models.Model):
    name = models.CharField(max_length=10)

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

def initialize():
    # Ensure the table is created and empty
    if os.path.exists('db.sqlite3'):
        os.unlink('db.sqlite3')
    django.db.connection.creation.create_test_db()

    # Populate the database
    for name in ['a', 'b', 'c']:
        MyModel.objects.create(name=name)

def run_test():
    initialize()

    group1 = MyModel.objects.filter(name='a')
    group2 = MyModel.objects.filter(name='b')
    group3 = MyModel.objects.filter(name='c')

    combined_group = group1.union(group2)
    group_and = combined_group & group1
    group_or = combined_group | group3  # Mistake corrected: group 3 -> group3, to match Python syntax

    try:
        assert combined_group.query != group_and.query, "The '&' operation did not modify the query."
        assert combined_group.query != group_or.query, "The '|' operation did not modify the query."
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Re-raise the exception to allow checking the assertion failure

if __name__ == '__main__':
    run_test()
```