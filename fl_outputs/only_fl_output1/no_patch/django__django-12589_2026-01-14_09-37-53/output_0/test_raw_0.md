```python
# reproducer.py
import os
import django
from django.db import models
from django.db.models import Count, Q, OuterRef, Subquery
from django.conf import settings
from django.core.management import execute_from_command_line

# Setting up Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


# Models definition
class A(models.Model):
    pass

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
    )
    status = models.IntegerField()

# Reproducing the issue described
def reproduce_issue():
    # Ensure the database schema is created
    execute_from_command_line(['manage.py', 'migrate'])

    # Setting up the data for the query
    b_instance = B.objects.create()
    a_instance = A.objects.create()
    AB.objects.create(a=a_instance, b=b_instance, status=10)
    C.objects.create(a=a_instance, status=5)

    # The described query
    try:
        ab_query = AB.objects.filter(a=OuterRef("pk"), b=b_instance.pk)
        filter_conditions = Q(pk=a_instance.pk) | Q(ab_a__b=b_instance.pk)
        query = A.objects.filter(filter_conditions).annotate(
            status=Subquery(ab_query.values("status")[:1]),
            c_count=Count("c"),
        )
        answer = query.values("status").annotate(total_count=Count("status"))
        # Attempt to execute the query
        print(answer.query)
        results = list(answer)

        # If no error occurred, the issue presumably has been resolved
        print("No error occurred:", results)
        exit(0)  # Exiting with code 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced") from e


# Stack trace printing function
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
    reproduce_issue()
```

This standalone script sets up a minimal Django environment within itself, creates the described models, and then tries to replicate the issue involving "GROUP BY" clauses. Please note that it works with SQLite by default, as specified in the `DATABASES` configuration, which might not behave identically to PostgreSQL in regard to the described error. If you're specifically interested in PostgreSQL, you would need to adjust the database settings appropriately and ensure your environment has the necessary dependencies installed.