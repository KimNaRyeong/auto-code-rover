Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import pickle
from django.conf import settings
from django.apps import apps
from django.db import models

# Configure Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[__name__]
)

apps.set_installed_apps(['reproducer'])

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
    # Create the tables
    models.Model.builtin_fields_cache.clear()
    apps.get_app_config(__name__).models_module = __name__
    models.base.Model._meta.db_table = 'reproducer_modela'
    with apps.registry.autodiscover():
        ModelA.objects.create(value='test')
    
    row = ModelA.objects.values_list('id', 'value', named=True).first()
    pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("django.db.models.query.Row is not pickleable")
```
This script configures Django, creates a model, inserts a record, retrieves it using `values_list` with `named=True`, and then tries to pickle the result. If the pickling fails, it prints the stack trace of the exception and raises an `AssertionError`.