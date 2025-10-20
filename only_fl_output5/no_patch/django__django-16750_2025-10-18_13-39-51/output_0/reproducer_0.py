# reproducer.py
import django
from django.conf import settings
from django.db import models
from django.db.models import Value
from django.db.models.functions import Chr

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

# Simulate minimal Django setup
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        __name__,  # Registers this app for models created during runtime
    ],
    USE_TZ=True,
)
django.setup()

# Define a simple model to use for the queryset
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = __name__

try:
    # Trying to reproduce the issue by annotating with Chr and a fixed value
    query = Author.objects.annotate(first_letter=Chr(Value(77)))
    query.first()  # Execute the query to make sure the error is raised during query evaluation
    
    # If the code reaches this point without an error, the problem is fixed/not reproducible
    print("Issue NOT reproduced; exit code 0 indicates the issue might be fixed or not present.")
except Exception as e:
    print_stacktrace(e)
    assert isinstance(e, ValueError), "Expected ValueError, found another exception."
    assert str(e) == "invalid literal for int() with base 10: 'M'", "The reproduced error message doesn't match expected."
