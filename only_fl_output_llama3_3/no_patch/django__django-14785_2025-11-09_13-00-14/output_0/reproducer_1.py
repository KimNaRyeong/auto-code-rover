import os
import sys
from django.db import models
from decimal import Decimal, getcontext
from django.core.exceptions import AssertionError

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

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    try:
        from django.conf import settings
        settings.configure()
        from django.db.models import DecimalField, Model
        class MyModel(Model):
            value = models.DecimalField(max_digits=10, decimal_places=5)
        getcontext().prec = 5
        obj = MyModel(value=float('nan'))
        obj.save(using='default')
        try:
            obj.refresh_from_db()
            assert True
        except TypeError as e:
            print_stacktrace(e)
            sys.exit(1)
    finally:
        settings._wrapped_settings = None

if __name__ == "__main__":
    main()
