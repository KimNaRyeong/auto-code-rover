from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import F

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
        class Document(models.Model):
            pass

        result = Document.objects.filter(
            checklist__isnull=False,
            part=OuterRef('id')
        ).values('checklist__customer', 'created').union(
            Document.objects.filter(
                ownershiptransfer__isnull=False,
                part=OuterRef('id')
            ).values('ownershiptransfer__ship_target__contact', 'created')
        ).annotate(owner=Subquery([]))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
