"""
reproducer.py
This script reproduces the issue where combining an empty Q object with a negated Exists object
does not correctly maintain the negation in Django's ORM query expressions.
"""

import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models, connections, DEFAULT_DB_ALIAS
from django.db.models import Exists, Q

def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Minimal Django settings required for the script to run.
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    USE_TZ=True,
)

django.setup()

class Book(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

def run_tests():
    # Create the necessary database tables.
    with connections[DEFAULT_DB_ALIAS].schema_editor() as schema_editor:
        schema_editor.create_model(Book)

    # Test case: Combining an empty Q with a negated Exists
    try:
        q = Q() & ~Exists(Book.objects.all())
        assert q.negated, "Combining an empty Q with a negated Exists should result in a negated Q object."
        print("Test passed: The issue is fixed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    run_tests()
