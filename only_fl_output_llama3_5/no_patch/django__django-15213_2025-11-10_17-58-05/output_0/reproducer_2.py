from django.db.models import Q, BooleanField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.query import QuerySet

def main():
    try:
        queryset = QuerySet()
        expression_wrapper = ExpressionWrapper(~Q(pk__in=[]), output_field=BooleanField())
        print(expression_wrapper)
        queryset.annotate(foo=expression_wrapper).values("foo").query
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

def print_stacktrace(e):
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
    main()
