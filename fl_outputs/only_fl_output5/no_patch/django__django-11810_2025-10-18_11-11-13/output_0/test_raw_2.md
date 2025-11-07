Given your request, I see now that the intent is to ensure the script fails under the current behavior (indicating a problem), but succeeds once the issue is fixed, signifying the problem doesn't persist. It seems there was a misunderstanding in my previous response about the expected behavior—from your description, the issue indeed involves unexpected mutation of the original queryset in Django due to chained `select_related` calls. Let's write a corrected script that accurately reproduits this issue and follows your specifications for error reporting:

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

# Define Django's runtime settings
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        "__main__",
    ),
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

# Define models
class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE, related_name='model_c_a')
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE, related_name='model_c_b')

# Prepare database
execute_from_command_line(['manage.py', 'migrate'])

try:
    query_1 = ModelC.objects.select_related('model_a')
    print('QUERY 1:', str(query_1.query))
    
    query_2 = query_1.select_related('model_b')
    print('QUERY 2:', str(query_2.query))
    
    assert str(query_1.query) != str(query_2.query), "Chaining select_related mutates original QuerySet."

except AssertionError as e:
    print("AssertionError: The issue has been reproduced.")
    print_stacktrace(e)
    sys.exit(1)  # Exit with error to indicate failure in reproducing/identifying the issue

print("Success: Issue is not present or has been fixed.")
sys.exit(0)  # Exit with code 0 to indicate success/no error
```

In this script, we're setting up a minimal Django environment programmatically, defining models that mimic your described setup, and then running a test that creates two querysets from `ModelC`, chaining `select_related` in a way that would expose the mutation issue if present.

The script specifically checks for mutation of the original queryset (`query_1`) after chaining another `select_related` call with `query_2`. Using the assertion check, it raises an error when the two queries are the same after such operations, indicating that `query_1` has been unexpectedly mutated. Conversely, if the issue isn't present (meaning the two query strings remain different, as they should), the script exits with code 0, indicating the issue is either fixed or not reproducible under the described conditions.
