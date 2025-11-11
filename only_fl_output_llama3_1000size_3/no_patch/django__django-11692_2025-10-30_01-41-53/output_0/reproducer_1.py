from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import F
from django.db.models.query import Q

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
        Document.objects.filter(checklist__isnull=False, part=OuterRef('id')).values('checklist__customer', 'created')
        Document.objects.filter(ownershiptransfer__isnull=False, part=OuterRef('id')).values('ownershiptransfer__ship_target__contact', 'created')
        return self.annotate(owner=Subquery((Document.objects.filter(checklist__isnull=False, part=OuterRef('id')).union(Document.objects.filter(ownershiptransfer__isnull=False, part=OuterRef('id'))).values('owner')[:1])))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
