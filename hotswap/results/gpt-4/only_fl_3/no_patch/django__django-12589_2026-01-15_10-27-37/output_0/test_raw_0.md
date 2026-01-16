```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models, connections
from django.db.models import Count, Subquery, OuterRef, Q
from django.db.utils import ProgrammingError

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

# Define Mock Models
class A(models.Model):
    pass

class B(models.Model):
    pass

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

class C(models.Model):
    a = models.ForeignKey(A, null=True, blank=True, on_delete=models.SET_NULL, related_name="c")
    status = models.IntegerField()

# Settings configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
    }
}

settings.configure(
    DATABASES=DATABASES,
    INSTALLED_APPS=[
        __name__,
    ],
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

# Create tables
with connections['default'].schema_editor() as editor:
    editor.create_model(A)
    editor.create_model(B)
    editor.create_model(AB)
    editor.create_model(C)

# Attempt reproducing the issue
try:
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values("status")[:1]),
        c_count=Count("c"),
    )

    answer = query.values("status").annotate(total_count=Count("status"))

    # Evaluating queryset
    list(answer)  

    # If the control reaches this point, the issue has been resolved
    print("The issue has been resolved.")
    exit(0)

except ProgrammingError as e:
    print_stacktrace(e)
    assert "column reference \"status\" is ambiguous" in str(e), "Error does not match known issue."
    # The AssertionError is expected when the issue is present.
except Exception as e:
    print("An unexpected error occurred.")
    print_stacktrace(e)

# If here, then an error was caught; exiting with non-zero indicates failure
exit(1)
```