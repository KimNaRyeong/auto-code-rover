Here is the `reproducer.py` file that reproduces the issue:
```
import os
from django.db import models
from django.db.models.functions import ExtractYear
from django.core.exceptions import ValidationError

# Create a test model with a DurationField
class MyModel(models.Model):
    duration = models.DurationField()

def setup_test_db():
    # Create the test database
    from django.test.utils import setup_test_environment
    setup_test_environment()
    from django.db.backends.sqlite3.base import DatabaseWrapper
    db_wrapper = DatabaseWrapper('sqlite:///:memory:')
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE mymodel (id INTEGER PRIMARY KEY, duration INTERVAL)")

def main():
    # Create the test model table
    setup_test_db()

    # Try to annotate and filter on ExtractYear of a DurationField
    try:
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        raise AssertionError("Expected ValueError or ValidationError, but no exception was raised")
    except (ValueError, ValidationError) as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
This script creates a test model with a `DurationField`, sets up an in-memory SQLite database, and then tries to annotate and filter on the `ExtractYear` of the `DurationField`. If no exception is raised, it raises an `AssertionError`. If a `ValueError` or `ValidationError` is raised, it prints the stack trace using the provided function.