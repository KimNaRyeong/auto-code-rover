import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.apps import apps

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # This script is the app
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
)

apps.populate(settings.INSTALLED_APPS)

class MyModel(models.Model):
    name = models.CharField(max_length=255)

# Mimic manage.py environment
execute_from_command_line(['manage.py', 'migrate'])

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

def test_exists_subquery_with_empty_queryset_issue():
    try:
        qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
        assert str(qs.query).find('WHERE') != -1, "WHERE block is missing from the query."
        print("No issue found, the WHERE block exists.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present")

if __name__ == '__main__':
    test_exists_subquery_with_empty_queryset_issue()
