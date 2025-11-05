import django
from django.db import models
from django.db.models import Case, When, Q, Value, Exists

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

try:
    class State(models.Model):
        pass

    class County(models.Model):
        name = models.CharField(max_length=50)
        state = models.ForeignKey(State, related_name='counties')

    django.setup()

    # This should raise an error
    County.objects.annotate(
        status=Case(
            When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), then=Value("DALLAS COUNTY")),
            default=Value("ELSEWHERE"),
        )
    )

except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error"

print("Issue not present")
exit(0)
