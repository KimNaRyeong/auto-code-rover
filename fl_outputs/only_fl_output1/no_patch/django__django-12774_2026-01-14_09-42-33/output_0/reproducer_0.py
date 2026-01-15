# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

# Minimal setup for Django
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

class Article(models.Model):
    slug = models.CharField(max_length=255)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_slug")
        ]

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

# Entry point for testing the issue
def test_in_bulk_with_unique_constraint():
    try:
        # Attempt to retrieve objects in_bulk using a field with unique constraint but not `unique=True`
        Article.objects.in_bulk(field_name="slug")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

if __name__ == '__main__':
    # Create tables for the test models
    django.core.management.call_command('migrate', verbosity=0, interactive=False)
    
    # Run the test
    test_in_bulk_with_unique_constraint()
