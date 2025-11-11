import os
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

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

if __name__ == "__main__":
    try:
        class MyModel(models.Model):
            value = models.DecimalField(max_digits=10, decimal_places=5)

        obj = MyModel(value="nan")
        obj.save()
        MyModel.objects.get(pk=1)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected exception not raised"

    print("Issue reproduced successfully.")
