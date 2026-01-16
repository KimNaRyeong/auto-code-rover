Given the details of your request and the context surrounding the initial failure to execute the test script, I'll provide you with an updated version of the `reproducer.py` script. This script should now better encapsulate the Django environment setup, model creation, and execution flow. It aims to reproduce the reported Django 3.0.4 "GROUP BY" clauses error.

Please make sure to run this script in an environment where Django is properly installed and accessible. Also, adjust the database settings according to your actual database setup if you're not using SQLite.

```python
import os
import sys
import django
from django.db import models, ProgrammingError
from django.db.models import Count, Q, Subquery, OuterRef
from django.conf import settings

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

def setup_django_environment():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=[
            "__main__",
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

class A(models.Model):
    class Meta:
        app_label = "__main__"

class B(models.Model):
    class Meta:
        app_label = "__main__"

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

    class Meta:
        app_label = "__main__"

class C(models.Model):
    a = models.ForeignKey(A, null=True, blank=True, on_delete=models.SET_NULL, related_name="c")
    status = models.IntegerField()

    class Meta:
        app_label = "__main__"

def execute_query():
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values("status")),
        c_count=Count("c"),
    )
    answer = query.values("status").annotate(total_count=Count("status"))
    return answer

if __name__ == "__main__":
    setup_django_environment()

    try:
        models.Model.check(force_reload=True)
        from django.db import connection
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(A)
            schema_editor.create_model(B)
            schema_editor.create_model(AB)
            schema_editor.create_model(C)

        answer = execute_query()
        print(answer.query)  # This prints the query for inspection.

        # Attempt to evaluate the query.
        list(answer)
    except ProgrammingError as e:
        print_stacktrace(e)
        assert "column reference \"status\" is ambiguous" in str(e), "The issue should be present under Django 3.0.4 with PostgreSQL"
    else:
        print("The issue seems to be resolved.")
        sys.exit(0)
    sys.exit(1)
```

This script is designed to be self-contained and should be run in a Django-supported environment. Note that this specific script uses SQLite for simplicity, which might not reproduce the error in the same way a PostgreSQL database would, given the error description relates to a PostgreSQL-specific issue. For an accurate reproduction of the issue, ensure a PostgreSQL database is configured within the `DATABASES` setting in the script.