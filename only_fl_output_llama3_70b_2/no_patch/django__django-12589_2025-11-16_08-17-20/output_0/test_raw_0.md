Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count

# Create a new Django project and app
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
import reproducer.settings as settings
settings.configure()

from django.apps import apps
apps.populate(settings.INSTALLED_APPS)

# Define the models
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
    # Create the database tables
    models.Model.__subclasses__()  # Force model registration
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE test_app_a (id SERIAL PRIMARY KEY);")
        cursor.execute("CREATE TABLE test_app_b (id SERIAL PRIMARY KEY);")
        cursor.execute("""
            CREATE TABLE test_app_ab (
                id SERIAL PRIMARY KEY,
                a_id INTEGER NOT NULL REFERENCES test_app_a(id),
                b_id INTEGER NOT NULL REFERENCES test_app_b(id),
                status INTEGER NOT NULL
            );
        """)
        cursor.execute("CREATE TABLE test_app_c (id SERIAL PRIMARY KEY, a_id INTEGER REFERENCES test_app_a(id), status INTEGER);")

    # Insert some data
    A.objects.create(id=1)
    B.objects.create(id=1)
    AB.objects.create(a_id=1, b_id=1, status=1)
    C.objects.create(a_id=1, status=1)

    # Evaluate the query
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values("status")),
        c_count=Count("c"),
    )
    answer = query.values("status").annotate(total_count=Count("status"))

    # This should raise a ProgrammingError
    list(answer)

except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
else:
    sys.exit(0)
```
This script creates the necessary database tables and inserts some data. Then it evaluates the query that causes the issue. If the issue is present, it raises an `AssertionError` with a stack trace of the error. If the issue is fixed, the script exits with code 0.