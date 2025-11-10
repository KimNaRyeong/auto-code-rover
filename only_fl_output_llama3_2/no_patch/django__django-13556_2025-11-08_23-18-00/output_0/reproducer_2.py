import django
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

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

def reproducer():
    try:
        transaction.on_commit(None)  # This line should raise an error
        print("Transaction committed")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError: 'NoneType' object is not callable."

if __name__ == "__main__":
    reproducer()
