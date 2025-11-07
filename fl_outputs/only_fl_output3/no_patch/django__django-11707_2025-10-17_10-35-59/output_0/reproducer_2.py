"""
reproducer.py
-------------
This script is designed to be run in a Django project root directory.
It reproduces an issue where pickling a QuerySet evaluates querysets given to Subquery in annotate,
leading to unexpected database queries or errors.
"""

import pickle
from django.db import models
from django.db.models import Exists, OuterRef
from django.conf import settings
import django

# Minimal Django settings. Adjust as necessary for your project.
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        '__main__',  # Allows this script's models to be recognized by Django
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',  # Using an in-memory database for simplicity
        }
    },
    USE_TZ=True,
)
django.setup()

# Defining minimal models required to reproduce the issue
class Group(models.Model):
    name = models.CharField(max_length=100)

class Event(models.Model):
    group = models.ForeignKey(Group, related_name='events', on_delete=models.CASCADE)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        print(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}', file=sys.stderr)
        print(f"    {frame.line}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Simulating the situation described in the issue
    try:
        groups = Group.objects.annotate(
            has_event=models.Exists(Event.objects.filter(group_id=models.OuterRef('id')))
        )
        with django.test.TestCase().assertNumQueries(0):
            pickle.loads(pickle.dumps(groups.query))
        print("No AssertionError, the issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The intended behavior did not occur as expected.")

if __name__ == "__main__":
    main()
