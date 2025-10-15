import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Exists, OuterRef, Q

# Minimal Django setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script will be the app
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define a simple model
class Book(models.Model):
    title = models.CharField(max_length=100)

# Utility for printing stack trace
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

# Main check
try:
    # Simulate test conditions
    q1 = Q() & Exists(Book.objects.all())
    assert not q1.negated, "Combining an empty Q with an Exists doesn't negate as expected."

    q2 = Q() & ~Exists(Book.objects.all())
    assert q2.negated, "Combining an empty Q with a negated Exists does not preserve negation."

    print("Test passed. No issue found.")
except AssertionError as ae:
    print_stacktrace(ae)
    exit(1)  # Exit with an error status
