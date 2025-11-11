import django
from django.db.models import Q, Case, When, Value, BooleanField
from django.db.models.functions import Coalesce

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
        User = type('User', (), {'objects': None})
        User.objects.annotate(
            _a=Case(
                When(~Q(pk__in=[]), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by("-a").values("pk")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected behavior not achieved")

if __name__ == "__main__":
    main()
