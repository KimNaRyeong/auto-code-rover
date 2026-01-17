# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
import pickle

# Configure Django for standalone scripts
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This script is the 'app'
    ],
)

django.setup()

# Define models to use in the test
class Group(models.Model):
    name = models.CharField(max_length=100)

class Event(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

# Ignore the System Checks for missing apps, not the point of this reproducer
from django.core.management import call_command
call_command('migrate', verbosity=0, skip_checks=True)

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

def main():
    try:
        # Create query as described in issue
        groups = Group.objects.annotate(
            has_event=models.Exists(Event.objects.filter(group_id=models.OuterRef('id')))
        )
        # Attempt to pickle the query to reproduce the issue
        with open(os.devnull, 'wb') as f:
            f.write(pickle.dumps(groups.query))  # Should not evaluate the queryset
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        raise AssertionError("Failed due to an unexpected exception.") from e
    else:
        print("The issue could not be reproduced, or it has been fixed.")

if __name__ == "__main__":
    main()
