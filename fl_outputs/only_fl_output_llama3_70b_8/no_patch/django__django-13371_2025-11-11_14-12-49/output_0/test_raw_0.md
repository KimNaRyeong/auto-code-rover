Here is the `reproducer.py` file that reproduces the issue:
```
import pickle
from django.db import models
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=('reproducer', )
)

class ModelA(models.Model):
    value = models.CharField(max_length=12)

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

try:
    models.Model._meta.db_table = 'reproducer_modela'
    ModelA.objects.create(value='test')
    row = ModelA.objects.values_list('id', 'value', named=True).first()
    pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("django.db.models.query.Row is not pickleable")
```
This script creates a Django model, inserts a row into the database, retrieves the row using `values_list` with `named=True`, and then tries to pickle the resulting `Row` object. If the pickling fails (which it should), it prints the stack trace of the exception and raises an `AssertionError`.