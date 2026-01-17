```python
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Count, Q, Subquery, OuterRef
from django.core.management.commands.migrate import Command as MigrateCommand

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
    USE_I18N=True,
    USE_L10N=True,
)

django.setup()

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
        related_name="c"
    )
    status = models.IntegerField()

MigrateCommand().execute()

# Dummy Data Insertion for Reproduction
a_instance = A.objects.create()
b_instance = B.objects.create()
AB.objects.create(a=a_instance, b=b_instance, status=1)
C.objects.create(a=a_instance, status=1)

# Evaluation of the Query
try:
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=b_instance.pk)
    filter_conditions = Q(pk=a_instance.pk) | Q(ab_a__b=b_instance.pk)
    query = A.objects.\
        filter(filter_conditions).\
        annotate(
            status=Subquery(ab_query.values("status")),
            c_count=Count("c"),
    )
    answer = query.values("status").annotate(total_count=Count("status"))
    assert "GROUP BY" in str(answer.query), "Query did not generate a GROUP BY clause"
    print(answer)
except AssertionError as e:
    raise
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("No issue, the query works as expected.")
    SystemExit(0)
```

This script is a standalone Python script named `reproducer.py`, which can be placed in the root directory of a Django project and executed with `python3 reproducerer.py` to reproduce the described issue. It first configures a minimal Django environment, defines models according to the given issue, migrates the database, inserts dummy data, and then attempts to run the problematic query. If the issue is present (e.g., "GROUP BY" clause error like an `AssertionError` or any other unexpected exception), it tries to assert the presence of a "GROUP BY" clause in the constructed query, catches the exception, prints a detailed stack trace, and exits with code `1`. If the query executes without any errors, indicating the issue might have been resolved in the current or a newer Django version than initially reported, it will print a success message and exit with code `0`.