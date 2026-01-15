Below is the `reproducer.py` Python script designed to reproduce the described issue. This script assumes you have Django and PostgreSQL set up correctly in your environment. The script programmatically creates a Django setting environment, defines models as per the description, applies migrations to create these models in the database, and finally, executes the problematic query. If the issue exists, `AssertionError` will be raised, and the script will print a detailed stack trace as requested. Otherwise, it will exit with code 0, indicating the issue is fixed or not present.

```python
import os
import django
from django.db import models
from django.db.models import Q, Count
from django.db.models.expressions import OuterRef, Subquery
from django.core.management.commands.migrate import Command as MigrateCommand
from django.conf import settings

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This module (reproducer.py) will be treated as an app by Django
    ),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    SECRET_KEY='reproducer_secret_key',
    BASE_DIR=BASE_DIR,
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
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
    a = models.ForeignKey(A, null=True, blank=True, on_delete=models.SET_NULL, related_name="c")
    status = models.IntegerField()

# Apply migrations (in memory for SQLite)
MigrateCommand().execute(database='default', interactive=False, verbosity=0)

# Attempt to reproduce the issue
def reproduce_issue():
    try:
        ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
        filter_conditions = Q(pk=1) | Q(ab_a__b=1)
        query = A.objects.\
            filter(filter_conditions).\
            annotate(
                status=Subquery(ab_query.values("status")[:1]),
                c_count=Count("c"),
            )
        answer = query.values("status").annotate(total_count=Count("status"))
        print(answer.query)
        print(answer)
        # If the query executes without error, assert failure as issue should cause error
        raise AssertionError("The expected 'ProgrammingError' due to ambiguous 'GROUP BY' was not raised.")
    except Exception as e:
        print_stacktrace(e)

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

if __name__ == '__main__':
    reproduce_issue()
```

Replace `'your_db_name'`, `'your_db_user'`, and `'your_db_password'` with the actual credentials for your PostgreSQL database. This script does not handle the creation of the database itself, so ensure the database exists before executing the script.

The script mimics the functionality of a minimal Django project and should only be used in a controlled, development environment given its intent for debugging an issue. Always double-check configurations, especially when interacting with databases.