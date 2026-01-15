```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models, migrations, connections
from django.db.models import Count, Q, OuterRef, Subquery
from django.core.management.color import no_style


def setup_django_environment():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            '__main__',
        ),
    )
    django.setup()


# Models:
class A(models.Model):
    class Meta:
        app_label = '__main__'

class B(models.Model):
    class Meta:
        app_label = '__main__'

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, related_name="ab_a")
    b = models.ForeignKey(B, on_delete=models.CASCADE, related_name="ab_b")
    status = models.IntegerField()

    class Meta:
        app_label = '__main__'

class C(models.Model):
    a = models.ForeignKey(A, null=True, blank=True, on_delete=models.SET_NULL, related_name="c")
    status = models.IntegerField()

    class Meta:
        app_label = '__main__'


def run_migrations():
    # Create the tables in the database
    connection = connections['default']
    with connection.schema_editor() as schema_editor:
        for model in [A, B, AB, C]:
            schema_editor.create_model(model)


def reproduce_issue():
    try:
        # Populate database
        b = B.objects.create()
        a = A.objects.create()
        AB.objects.create(a=a, b=b, status=10)
        C.objects.create(a=a, status=5)

        # Define query
        ab_query = AB.objects.filter(a=OuterRef("pk"), b=b.pk)
        filter_conditions = Q(pk=a.pk) | Q(ab_a__b=b.pk)
        query = A.objects.filter(filter_conditions).annotate(
            status=Subquery(ab_query.values("status")[:1], output_field=models.IntegerField()),
            c_count=Count("c"),
        )
        answer = query.values("status").annotate(total_count=Count("status"))
        
        print(answer.query)
        print(list(answer))

        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced") from e


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


if __name__ == '__main__':
    setup_django_environment()
    run_migrations()
    reproduce_issue()
```

This script initializes a minimal Django environment with the models as described in the issue, runs migrations to create those models in a SQLite database, and attempts to reproduce the error. When executed, it should raise an `AssertionError` if the issue is reproducible, showing a stack trace of the original error, or it will exit with code 0, indicating the issue could not be reproduced under this setup.

Please note, the `run_migrations()` function programmatically creates the models in the database avoiding the Django migrations system formalities for a quick setup, which is more suitable for reproducing such issues without needing a complete Django project setup. 
