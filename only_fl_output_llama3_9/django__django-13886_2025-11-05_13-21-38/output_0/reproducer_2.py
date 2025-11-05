import django
from django.db.models import F, IntegerField
from django.db.models.indexes import Index

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
    try:
        from django.db.models import Q
        class MyModel(django.db.models.Model):
            foo = IntegerField()
            bar = F('non_existent_field')
        Index(fields=['foo'], name='my_index')
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected AssertionError"

if __name__ == "__main__":
    main()
