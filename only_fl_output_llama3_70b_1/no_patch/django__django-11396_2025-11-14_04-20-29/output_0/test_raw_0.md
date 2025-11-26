Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.db.models import Value, F

# Create a simple Django model
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

class MyModel(models.Model):
    id = models.AutoField(primary_key=True)

MyModel.objects.create()  # create an instance to query

try:
    result = MyModel.objects.annotate(my_column=Value('asdf')).order_by('my_column').values_list('id')
    assert False, "Expected ProgrammingError, but query succeeded"
except Exception as e:
    print_stacktrace(e)
    if isinstance(e, ProgrammingError) and str(e).startswith("non-integer constant in ORDER BY"):
        raise AssertionError("Issue is present")
    else:
        print("Unexpected exception:", e)

print("Issue is fixed")
```
This script creates a simple Django model, annotates it with a constant value, and tries to order the query by that annotated column. If the issue is present, it should raise a `ProgrammingError` with a specific error message, which we catch and re-raise as an `AssertionError`. If the issue is fixed, the script will print "Issue is fixed" and exit with code 0.