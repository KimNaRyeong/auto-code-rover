Here is the reproducer script:

```python
import os
from django.db import IntegrityError, ProgrammingError
from django.db.models import Count, Q, OuterRef
from django.db.models.functions import Subquery
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
            raise AssertionError("ProgrammingError raised")
        except IntegrityError as e:
            print_stacktrace(e)
            raise AssertionError("IntegrityError raised")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    suite = unittest.TestLoader().loadTestsFromTestCase(ReproducerTestCase)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        print_stacktrace(result.failures[0])
        sys.exit(1)

import unittest
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    import sys
```

This script will run the test case and if any error occurs, it will print the stack trace and raise an `AssertionError`.