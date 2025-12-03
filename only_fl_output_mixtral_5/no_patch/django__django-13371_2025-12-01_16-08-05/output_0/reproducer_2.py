import pickle
from django.core.exceptions import ImproperlyConfigured
from django.db import models
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    class ModelA(models.Model):
        value = models.CharField(max_length=12)

    row = ModelA.objects.values_list('id', 'value', named=True).first()
    pickled_row = pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    assert False, "An exception occurred while pickling Row object"
except ImproperlyConfigured:
    print("Django is not properly configured", file=sys.stderr)
    sys.exit(1)
