Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys

from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

class A(models.Model):
    bs = models.ManyToManyField('B', related_name="a", through="AB")

class B(models.Model):
    pass

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

class C(models.Model):
    a = models.ForeignKey(
        A,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="c",
        verbose_name=_("a")
    )
    status = models.IntegerField()

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values("status")),
        c_count=Count("c"),
    )
    answer = query.values("status").annotate(total_count=Count("status"))
    print(answer.query)
    result = list(answer)  # Evaluate the query
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")

sys.exit(0)
```
This script defines the models, creates the query, and evaluates it. If an exception occurs during the evaluation, it prints the stack trace using the provided `print_stacktrace` function and raises an `AssertionError`. If no exception occurs, the script exits with code 0.

Note that you need to create a `reproducer` directory with a `settings.py` file containing the necessary Django settings for this script to work.