from django.db.models import F
import sys

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

try:
    # Create a simple Django model
    from django.db import models

    class MyModel(models.Model):
        some_field = models.CharField(max_length=255)

    # This should raise an error if the issue is present
    MyModel.objects.filter(F('some_field').lower() == 'anssi')
    print("Issue is fixed")
    sys.exit(0)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is still present")
