import pickle
from django.db import models
from django.db.models import Value

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
    class ModelA(models.Model):
        value = models.CharField(max_length=12)

    row = ModelA.objects.values_list('id', 'value', named=True).first()
    pickle.dumps(row)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected the script to run without raising an exception"
    exit(1)
