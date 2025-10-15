"""
reproducer.py
"""

# Ensure Django settings are configured before importing ORM components
import os
import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=("__main__",),
    USE_TZ=True,
)

django.setup()

from django.db import models
from django.db.models import Sum, Value, ExpressionWrapper, IntegerField

# Define a simple model to work with
class Model(models.Model):
    column_a = models.IntegerField()
    column_b = models.IntegerField()

    class Meta:
        app_label = '__main__'

# Setting up the database (for demonstration purposes, in memory would be better for real tests)
from django.core.management import call_command
call_command("migrate", run_syncdb=True)

def execQuery(expr):
    try:
        expr = ExpressionWrapper(expr, output_field=IntegerField())
        return Model.objects.annotate(expr_res=expr).values('expr_res', 'column_a').annotate(sum=Sum('column_b'))
    except Exception as e:
        raise e

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

def test_query():
    # Simulating the issue
    try:
        query_result = execQuery(Value(3))  # Constant expression
        print("Query executed, attempting to fetch results to trigger evaluation...")
        list(query_result)  # Forces evaluation of the QuerySet
        # If no exception occurred, the issue is presumably fixed
        print("Test passed: No issue detected. Exiting normally.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert "GROUP BY" in str(e), "Expected issue about GROUP BY not found."
        print("Test failed: Issue detected as expected.")
        sys.exit(1)

if __name__ == "__main__":
    test_query()
