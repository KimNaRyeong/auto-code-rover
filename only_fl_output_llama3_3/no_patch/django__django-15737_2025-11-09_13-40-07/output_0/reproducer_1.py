import django
from django.db import models
from django.db.models.fields.related import ForeignKey
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

def reproduce_issue():
    try:
        django.setup()
        from .models import Parent, Child
        parent = Parent(name='parent_object')
        child = Child(parent=parent)
        parent.save()
        child.save()
        if child.parent.name != 'parent_object':
            raise AssertionError("Lazy read of the parent object occurred")
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
