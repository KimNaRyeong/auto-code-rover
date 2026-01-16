# reproducer.py
import decimal
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line

# Configuration for Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

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

def test_invalid_decimal_query():
    execute_from_command_line(['manage.py', 'migrate'])
    try:
        DecimalModel.objects.get(dec_field='12345')
        assert False, "Query with decimal larger than max_digits should not be executed without raising an exception."
    except decimal.InvalidOperation:
        # Expected failure for this issue
        raise
    except DecimalModel.DoesNotExist:
        # Expected behavior when the issue is fixed
        pass

if __name__ == '__main__':
    try:
        test_invalid_decimal_query()
        print("Test passed: the issue has been fixed.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Test failed: the issue is still present."
