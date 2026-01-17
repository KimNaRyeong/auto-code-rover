Given the feedback and the requirements to both reproduce the error specifically for the Django 3.0.4 "GROUP BY" issue within a PostgreSQL context, as well as ensuring the environment is correctly initialized before models are defined, the standalone script `reproducer.py` below has been restructured to meet these needs. This version should be compatible with Django's expectations for settings configuration, model definition, and database access, which are critical for reproducing database-specific behaviors like the one described. Make sure your database settings are configured for PostgreSQL.

```python
"""
reproducer.py
"""
import django
from django.conf import settings
from django.db import models, ProgrammingError
from django.db.models import Count, Q, Subquery, OuterRef

def setup_django():
    settings.configure(
        INSTALLED_APPS=["__main__"],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'your_db_name',
                'USER': 'your_db_user',
                'PASSWORD': 'your_db_password',
                'HOST': 'localhost',  # Set to your database host
                'PORT': '5432',
            }
        },
        USE_TZ=True,
    )
    django.setup()

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

# Setup Django before defining models
setup_django()

class A(models.Model):
    pass

class B(models.Model):
    pass

class AB(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE)
    b = models.ForeignKey(B, on_delete=models.CASCADE)
    status = models.IntegerField()

class C(models.Model):
    a = models.ForeignKey(A, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField()

def reproduce_issue():
    ab_query = AB.objects.filter(a=OuterRef("pk"), b=1)
    filter_conditions = Q(pk=1) | Q(ab__b=1)
    query = A.objects.filter(filter_conditions).annotate(
        status=Subquery(ab_query.values('status')[:1]),
        c_count=Count('c'),
    ).values('status').annotate(total_count=Count('status'))
    try:
        print(query.query)
        print(list(query))
    except ProgrammingError as e:
        print_stacktrace(e)
        raise AssertionError("The issue has not been fixed yet.")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue seems to be resolved, exiting with code 0.")
        sys.exit(0)
```

**Note:** Before running this script, replace `'your_db_name'`, `'your_db_user'`, and `'your_db_password'` with your actual PostgreSQL database credentials. This script aims to directly reproduce the issue based on the original description involving Django's handling of "GROUP BY" clauses in a PostgreSQL environment.

This approach ensures Django's settings are properly configured before any models are instantiated. Furthermore, it encapsulates the issue reproduction logic within the `reproduce_issue` function and correctly exits with status `0` only if the identified issue has been resolved, thereby aligning with the stipulated requirements.