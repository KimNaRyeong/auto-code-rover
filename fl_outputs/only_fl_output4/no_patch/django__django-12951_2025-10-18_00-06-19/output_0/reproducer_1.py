# reproducer.py
import os
import django
from django.conf import settings
from django.db import models, connections, OperationalError
from django.db.models import Case, When, Value, Exists, OuterRef, Q

# Minimal configuration for Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This module (a quirk of how we're running things)
    ),
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

# Define models
class State(models.Model):
    class Meta:
        app_label = '__main__'

class County(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, related_name='counties', on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'

# Function to print exceptions in a readable format
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
      
def create_tables():
    with connections['default'].schema_editor() as schema_editor:
        schema_editor.create_model(State)
        schema_editor.create_model(County)

# Main function to reproduce the issue
def main():
    # Dynamically create tables for our models
    create_tables()

    # Prepare test data
    try:
        texas = State.objects.create()
        County.objects.create(name="Dallas", state=texas)

        # Attempt to use When with Exists as outlined in the issue description
        annotated_counties = County.objects.annotate(
            status=Case(
                When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas", then=Value("DALLAS COUNTY")),
                default=Value("ELSEWHERE"),
            )
        )
        for county in annotated_counties:
            # Just forcing evaluation of the queryset
            pass

        print("Issue not reproduced - execution successful.")

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An error occurred attempting to reproduce the issue.") from e

if __name__ == '__main__':
    main()
