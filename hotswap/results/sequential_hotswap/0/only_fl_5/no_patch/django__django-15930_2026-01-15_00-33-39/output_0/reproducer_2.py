"""
reproducer.py

This script attempts to replicate the described Django issue with Case() and ~Q(pk__in=[]).
"""
import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Case, When, Value, Q, BooleanField

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

# Set up Django environment
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Define a minimal User model to test the Case() and Q() interaction
class User(models.Model):
    username = models.CharField(max_length=255)

    class Meta:
        app_label = '__main__'


def main():
    try:
        # Ensure the database table exists
        User.objects.all().delete()

        # Reproduce the issue
        result = User.objects.annotate(
            _a=Case(
                When(~Q(pk__in=[]), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by("-_a").values("pk")

        print(list(result))  # Attempt to evaluate the queryset to trigger any errors

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced successfully.")

if __name__ == "__main__":
    main()
