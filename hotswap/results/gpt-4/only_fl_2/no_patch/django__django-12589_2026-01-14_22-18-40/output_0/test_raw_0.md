```python
import os
import django
from django.core.exceptions import ImproperlyConfigured
from django.db import models, ProgrammingError
from django.db.models import Count, Q, Subquery, OuterRef
from django.conf import settings

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

def setup():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            '__main__',
        ),
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        ROOT_URLCONF=None,
    )

    try:
        django.setup()
    except ImproperlyConfigured as e:
        print("Django improperly configured:", e)
        exit(1)

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

def execute_query():
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab_a__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values("status")),
        c_count=Count("c"),
    )
    answer = query.values("status").annotate(total_count=Count("status"))
    return answer

def main():
    setup()

    # Ensure models are created
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(A)
        schema_editor.create_model(B)
        schema_editor.create_model(AB)
        schema_editor.create_model(C)

    try:
        answer = execute_query()
        print(answer.query)  # Show the generated SQL query
        print(list(answer))  # Trigger the actual query evaluation
    except ProgrammingError as e:
        print_stacktrace(e)
        assert "column reference \"status\" is ambiguous" in str(e), "Unexpected error message"
    else:
        print("The issue is fixed.")
        exit(0)

if __name__ == "__main__":
    main()
```

This script does the following:
1. Sets up a minimal Django environment.
2. Defines the models as per the issue description.
3. Constructs and executes the problematic query.
4. Catches and prints the stack trace for the `ProgrammingError`.
5. Exits with code 0 if the issue is fixed or raises an assertion error if the issue is present (via an ambiguous column reference in "GROUP BY" clause).

Please note, since the script uses Django model definitions and query constructions, it requires a Django project context to run properly. The script also assumes an SQLite database for simplicity and might not perfectly replicate the behavior with PostgreSQL as per the original issue description, especially considering database-specific behavior in "GROUP BY" clauses. However, it should be a good starting point for reproducing and diagnosing the described issue.