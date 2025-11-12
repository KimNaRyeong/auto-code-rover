import os
import sys
from django.db import models
from django.db.models import F, Max, Sum
from django.conf import settings

settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['__main__'],
)

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

from django.core.management import execute_from_command_line

execute_from_command_line(['', 'migrate'])

class T(models.Model):
    id = models.AutoField(primary_key=True)
    foo = models.IntegerField()

try:
    result = T.objects.annotate(anon=F('foo')).aggregate(foo=Max(F('anon')), sum=Sum(F('foo')))
    assert 'anon' in [field.name for field in result.keys()]
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
    sys.exit(0)
