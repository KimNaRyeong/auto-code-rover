import django
from django.db.models import Q, BooleanField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.query import QuerySet

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
        queryset = QuerySet()  # Create a query set
        result = queryset.annotate(foo=ExpressionWrapper(~Q(pk__in=[]), output_field=BooleanField()))
        print(result.values("foo").query)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
