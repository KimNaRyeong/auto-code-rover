Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
from django.db import IntegrityError, ProgrammingError
from django.db.models import Count, Q, Subquery, OuterRef
from django.db.models.functions import OuterRef
from django.test import TestCase

class ReproducerTestCase(TestCase):
    def test_reproducer(self):
        try:
            from models import A, B, AB, C  # Import the models
            ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
            filter_conditions = Q(pk=1) | Q(ab_a__b=1)
            query = A.objects.filter(filter_conditions).annotate(
                status=Subquery(ab_query.values("status")),
                c_count=Count("c"),
            )
            answer = query.values("status").annotate(total_count=Count("status"))
            print(answer.query)
            print(answer)
        except ProgrammingError as e:
            print_stacktrace(e)
            raise AssertionError("ProgrammingError occurred")
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError("IntegrityError occurred")

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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ReproducerTestCase().test_reproducer()

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.