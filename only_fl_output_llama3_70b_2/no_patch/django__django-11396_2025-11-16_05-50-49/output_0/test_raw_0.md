Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.db.models import Value
from django.db.models.functions import annotate

# Create a simple Django model
class MyModel(models.Model):
    id = models.AutoField(primary_key=True)

# Ensure the database is set up
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer.settings")
import django
django.setup()

try:
    # Attempt to execute the problematic query
    result = MyModel.objects.annotate(my_column=Value('asdf')).order_by('my_column').values_list('id')
    assert False, "Expected ProgrammingError, but query succeeded"
except Exception as e:
    print_stacktrace(e)
    if isinstance(e, ProgrammingError) and "non-integer constant in ORDER BY" in str(e):
        raise AssertionError("Issue is present")
    else:
        print("Unexpected exception:", file=sys.stderr)
        print_stacktrace(e)

print("Issue is fixed")
```
This script creates a simple Django model, sets up the database, and then attempts to execute the problematic query. If the query succeeds, it raises an `AssertionError`. If the query fails with a `ProgrammingError` containing the expected error message, it also raises an `AssertionError` indicating that the issue is present. If any other exception occurs, it prints the stack trace of the unexpected exception.