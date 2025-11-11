Here is the reproducer script:

```python
import os
from django.db import IntegrityError, ProgrammingError
from django.db.models import Count, Q, OuterRef
from django.db.models.functions import Subquery
from django.test import TestCase

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

class Reproducer(TestCase):
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
            self.assertTrue(True)  # This should not be reached
        except ProgrammingError as e:
            print_stacktrace(e)
            raise AssertionError("ProgrammingError raised") from None

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    Reproducer().run()  # Run the test