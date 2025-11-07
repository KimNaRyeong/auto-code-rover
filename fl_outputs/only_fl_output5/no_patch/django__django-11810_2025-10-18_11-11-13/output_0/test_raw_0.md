```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line

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

# Define in-memory database settings
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=(
        "__main__",
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define models
class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)

# Prepare database
execute_from_command_line(['manage.py', 'migrate'])

try:
    # Create queries
    query_1 = ModelC.objects.select_related('model_a')
    original_query_1_str = str(query_1.query)
    
    query_2 = query_1.select_related('model_b')
    original_query_2_str = str(query_2.query)
    
    if original_query_1_str == original_query_2_str:
        raise AssertionError("Chaining select_related mutates original QuerySet.")
    else:
        print("Issue not found. The queries are correctly isolated.")
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script checks if the described issue exists in a Django project environment. It attempts to reproduce the issue where applying `select_related` on a clone of a `QuerySet` mutates the original `QuerySet`. If the issue exists, it will raise an `AssertionError`, print a traceback specifying where the error occurred, and exit with code 1. If the issue is not present, it prints a confirmation message and exits with code 0. 

Ensure this script is named `reproducer.py` and placed in the root directory of a Django project to run it correctly. Also, remember to activate the project's virtual environment if necessary before executing the script with `python3 reproducer.py`.