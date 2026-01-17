import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models import Case, When, Value, BooleanField
from django.db.models.query_utils import Q

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Minimal Django setup for script to run
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script acts as a standalone app
    ),
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

class User(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Ensure the database exists and the model table is created
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(User)

    # Attempt to reproduce the issue
    try:
        User.objects.annotate(
            _a=Case(
                When(~Q(pk__in=[]), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by("-a").values("pk")
        print("The issue did not occur.")
        sys.exit(0)  # Exit code 0 for success scenario
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced.") from e
