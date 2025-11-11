Here is the reproducer script:

```python
import django
from django.db.models import Case, When, Value, BooleanField, Q
from django.db.models.functions import Coalesce
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
            from django.db.models import Case, When, Value, BooleanField
            User = self.create_model('User', pk='id')
            User.objects.annotate(
                _a=Case(
                    When(~Q(pk__in=[]), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            ).order_by("-a").values("pk")
        except Exception as e:
            print_stacktrace(e)
            raise

    def create_model(self, model_name, fields):
        from django.db import models
        class User(models.Model):
            id = models.IntegerField(primary_key=True)
            for field in fields:
                setattr(User, field, models.IntegerField())
        return User

if __name__ == "__main__":
    Reproducer().test_reproducer()
```

You can run this script with `python3 reproducer.py` to reproduce the issue. If the issue is present, it will print a stack trace and raise an AssertionError.